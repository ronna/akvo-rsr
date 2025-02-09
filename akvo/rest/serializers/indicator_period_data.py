# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.
import json

from rest_framework import serializers
from django.db.models import Sum
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

from akvo.rest.serializers.disaggregation import DisaggregationSerializer, DisaggregationReadOnlySerializer
from akvo.rest.serializers.rsr_serializer import BaseRSRSerializer
from akvo.rest.serializers.user import UserDetailsSerializer, UserRawSerializer
from akvo.rsr.models import (
    IndicatorPeriod, IndicatorPeriodData, IndicatorPeriodDataComment, IndicatorPeriodDataFile, IndicatorPeriodDataPhoto,
    IndicatorDimensionValue, Disaggregation
)
from akvo.utils import ensure_decimal


class IndicatorPeriodDataCommentSerializer(BaseRSRSerializer):

    user_details = UserDetailsSerializer(read_only=True, source='user')

    class Meta:
        model = IndicatorPeriodDataComment
        fields = '__all__'
        read_only_fields = ['user']


class IndicatorPeriodDataCommentNestedSerializer(BaseRSRSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = IndicatorPeriodDataComment
        fields = '__all__'
        read_only_fields = ('id', 'data', 'user')


class IndicatorPeriodDataFileSerializer(BaseRSRSerializer):
    class Meta:
        model = IndicatorPeriodDataFile
        fields = '__all__'


class IndicatorPeriodDataPhotoSerializer(BaseRSRSerializer):
    class Meta:
        model = IndicatorPeriodDataPhoto
        fields = '__all__'


class IndicatorPeriodDataSerializer(BaseRSRSerializer):

    user_details = UserDetailsSerializer(read_only=True, source='user')
    approver_details = UserDetailsSerializer(read_only=True, source='approved_by')
    status_display = serializers.ReadOnlyField()
    photo_url = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()

    class Meta:
        model = IndicatorPeriodData
        fields = '__all__'
        read_only_fields = ['user']


class IndicatorPeriodDataLiteSerializer(BaseRSRSerializer):

    user_details = UserRawSerializer(required=False, source='user')
    status_display = serializers.ReadOnlyField()
    photo_url = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    disaggregations = DisaggregationReadOnlySerializer(many=True, required=False)
    value = serializers.SerializerMethodField()
    file_set = IndicatorPeriodDataFileSerializer(many=True, read_only=True, source='indicatorperioddatafile_set')
    photo_set = IndicatorPeriodDataPhotoSerializer(many=True, read_only=True, source='indicatorperioddataphoto_set')
    comments = IndicatorPeriodDataCommentSerializer(read_only=True, many=True, required=False)

    def get_value(self, obj):
        return ensure_decimal(obj.value)

    class Meta:
        model = IndicatorPeriodData
        fields = (
            'id', 'user_details', 'status', 'status_display', 'update_method', 'value', 'numerator', 'denominator', 'text',
            'disaggregations', 'narrative', 'photo_url', 'file_url', 'period_actual_value', 'created_at', 'last_modified_at',
            'file_set', 'photo_set', 'review_note', 'comments',
        )


class IndicatorPeriodDataFrameworkSerializer(BaseRSRSerializer):

    period = serializers.PrimaryKeyRelatedField(queryset=IndicatorPeriod.objects.all())
    comments = IndicatorPeriodDataCommentNestedSerializer(many=True, required=False)
    disaggregations = DisaggregationSerializer(many=True, required=False)
    user_details = UserDetailsSerializer(read_only=True, source='user')
    approver_details = UserDetailsSerializer(read_only=True, source='approved_by')
    status_display = serializers.ReadOnlyField()
    photo_url = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    period_can_add_update = serializers.ReadOnlyField(source='period.can_save_update')
    files = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)
    photos = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)
    file_set = IndicatorPeriodDataFileSerializer(many=True, read_only=True, source='indicatorperioddatafile_set')
    photo_set = IndicatorPeriodDataPhotoSerializer(many=True, read_only=True, source='indicatorperioddataphoto_set')
    audit_trail = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorPeriodData
        fields = '__all__'
        read_only_fields = ['user']

    def get_audit_trail(self, obj):
        entries = LogEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(IndicatorPeriodData),
            object_id=obj.id,
            change_message__contains='"audit_trail": true'
        )
        return [
            {
                'user': {'id': entry.user.id, 'email': entry.user.email, 'first_name': entry.user.first_name, 'last_name': entry.user.last_name},
                'action_time': entry.action_time,
                'action_flag': 'CHANGE' if entry.action_flag == CHANGE else 'DELETION' if entry.action_flag == DELETION else 'ADDITION',
                'data': json.loads(entry.change_message)['data'],
            }
            for entry in entries
        ]

    def create(self, validated_data):
        self._validate_disaggregations(
            self._disaggregations_data,
            value=ensure_decimal(validated_data.get('value', 0)),
            numerator=ensure_decimal(validated_data.get('numerator', None)),
            denominator=ensure_decimal(validated_data.get('denominator', None))
        )
        """Over-ridden to handle nested writes."""
        files = validated_data.pop('files', [])
        photos = validated_data.pop('photos', [])
        comments = validated_data.pop('comments', [])
        update = super(IndicatorPeriodDataFrameworkSerializer, self).create(validated_data)
        for disaggregation in self._disaggregations_data:
            disaggregation['update'] = update.id
            if 'type_id' in disaggregation and 'dimension_value' not in disaggregation:
                disaggregation['dimension_value'] = disaggregation['type_id']
            serializer = DisaggregationSerializer(data=disaggregation)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
        for file in files:
            IndicatorPeriodDataFile.objects.create(update=update, file=file)
        for photo in photos:
            IndicatorPeriodDataPhoto.objects.create(update=update, photo=photo)
        for comment in comments:
            IndicatorPeriodDataComment.objects.create(data=update, user=update.user, comment=comment['comment'])

        return update

    def update(self, instance, validated_data):
        self._validate_disaggregations(
            self._disaggregations_data,
            value=ensure_decimal(validated_data.get('value', instance.value)),
            numerator=ensure_decimal(validated_data.get('numerator', instance.numerator)),
            denominator=ensure_decimal(validated_data.get('denominator', instance.denominator)),
            update=instance
        )
        """Over-ridden to handle nested updates."""
        files = validated_data.pop('files', [])
        photos = validated_data.pop('photos', [])
        comments = validated_data.pop('comments', [])
        super(IndicatorPeriodDataFrameworkSerializer, self).update(instance, validated_data)
        for disaggregation in self._disaggregations_data:
            disaggregation['update'] = instance.id
            serializer = DisaggregationSerializer(data=disaggregation)
            serializer.is_valid(raise_exception=True)
            disaggregation_instance, _ = instance.disaggregations.get_or_create(
                update=instance,
                dimension_value=serializer.validated_data['dimension_value'],
            )
            serializer.update(disaggregation_instance, serializer.validated_data)
        for file in files:
            IndicatorPeriodDataFile.objects.create(update=instance, file=file)
        for photo in photos:
            IndicatorPeriodDataPhoto.objects.create(update=instance, photo=photo)
        for comment in comments:
            comment_id = int(comment.get('id', 0))
            comment_txt = str(comment.get('comment', ''))
            if not comment_id:
                IndicatorPeriodDataComment.objects.create(data=instance, user=instance.user, comment=comment['comment'])
            else:
                comment_obj = IndicatorPeriodDataComment.objects.get(id=comment_id)
                if not comment_txt:
                    comment_obj.delete()
                else:
                    comment_obj.comment = comment_txt
                    comment_obj.save()

        return instance._meta.model.objects.select_related(
            'period',
            'user',
            'approved_by',
        ).prefetch_related(
            'comments',
            'disaggregations',
        ).get(id=instance.id)

    def _validate_disaggregations(self, disaggregations, value, numerator=None, denominator=None, update=None):
        adjustments = {}
        for disaggregation in disaggregations:
            type_id = disaggregation.get('type_id', disaggregation.get('dimension_value', None))
            if type_id is None:
                continue
            if denominator is not None:
                disaggregation_denominator = ensure_decimal(disaggregation.get('denominator', 0))
                if disaggregation_denominator > denominator:
                    raise serializers.ValidationError("disaggregations denominator should not exceed update denominator")
            category = IndicatorDimensionValue.objects.get(pk=type_id).name
            if category.id not in adjustments:
                adjustments[category.id] = {'values': 0, 'numerators': 0, 'type_ids': []}
            adjustments[category.id]['values'] += ensure_decimal(disaggregation.get('value', 0))
            adjustments[category.id]['numerators'] += ensure_decimal(disaggregation.get('numerator', 0))
            adjustments[category.id]['type_ids'].append(type_id)
        for key, adjustment in adjustments.items():
            unmodifieds = Disaggregation.objects.filter(update=update, dimension_value__name=key)\
                .exclude(dimension_value__in=adjustment['type_ids'])\
                .aggregate(values=Sum('value'))
            total = adjustment['values'] + ensure_decimal(unmodifieds['values'])
            if numerator is not None and adjustment['numerators'] > numerator:
                raise serializers.ValidationError("The disaggregation numerator should not exceed update numerator")
            if total > value:
                raise serializers.ValidationError("The accumulated disaggregations value should not exceed update value")

    def is_valid(self, raise_exception=False):
        # HACK to allow nested posting...
        self._disaggregations_data = self.initial_data.pop('disaggregations', [])
        super(IndicatorPeriodDataFrameworkSerializer, self).is_valid(raise_exception=raise_exception)
