import React from 'react'
import SimpleMarkdown from 'simple-markdown'
/* eslint-disable no-plusplus */
const lastCharEscape = ['.', ',', ';']
const escapeRegex = /\(([^)]+)\)\s\w+/g
const replace1 = /###/g
const replace2 = /·/g
const parse = SimpleMarkdown.defaultBlockParse
const mdOutput = SimpleMarkdown.defaultReactOutput

export const TrimText = ({ text, max = 400, isMarkdown = false }) => {
  if (text.length < max) {
    return <div>{isMarkdown ? mdOutput(parse(text)) : text}</div>
  }

  let escaped = []
  escaped = text.match(escapeRegex) || escaped
  escaped.forEach((x, i) => {
    const replacer = x.replace(/\s/g, '###')
    text = text.replace(x, replacer)
  })

  let arrayText = text.split(' ')
  arrayText = arrayText.filter((x) => x.length)
  text = ''
  let startIndex = 0

  while (text.length < max - 1 && arrayText[startIndex]) {
    text += `${arrayText[startIndex].replace(replace1, ' ').replace(replace2, '')} `
    startIndex++
  }
  text = text.slice(0, -1)

  if (text.slice(-1).match(/[0-9]/)) {
    text = text.slice(0, -1)
  }

  lastCharEscape.forEach((x) => {
    if (text.endsWith(x)) {
      text = text.slice(0, -1)
    }
  })

  return (
    <div>
      {isMarkdown ? mdOutput(parse(text)) : text}
      {' ... '}
    </div>
  )
}

export const titleCase = (str, delimiter = ' ') => {
  str = str.toLowerCase().split(delimiter)
  for (let i = 0; i < str.length; i++) {
    str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1)
  }
  return str.join(' ')
}

export const shortenText = (text, max) => {
  return text && text.length > max ? `${text.slice(0, max).split(' ').slice(0, -1).join(' ')}...` : text
}

export const convertToSlug = (Text) => {
  return Text.toLowerCase()
    .replace(/ /g, '-')
    .replace(/[^\w-]+/g, '')
}
