export const flagOrgs = {
  ENUMERATORS: new Set([43, 42]),
  NUFFIC: new Set([4531, 5255, 5722]),
  AKVO_USERS: new Set([42])
}

export const shouldShowFlag = (orgs, orgSet) => {
  return orgs && orgs.findIndex(it => orgSet.has(it.id) || orgSet.has(it.contentOwner)) !== -1
}

export const isRSRTeamMember = (userRdr) => {
  return userRdr.isSuperuser
}

export const isRSRAdmin = (userRdr) => {
  return userRdr?.isAdmin || userRdr?.isSuperuser
}
