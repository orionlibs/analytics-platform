import { AttributesMap, Model, Options, Preferences } from "./types"

export function getModel(
  element: HTMLElement,
  options: Options,
  preference: Preferences
): Model {
  const tag = element.tagName.toLowerCase()
  const text = getTextContent(element, preference)
  const attributes = getAttributes(element, options, preference)

  return {
    text,
    tag,
    isNotable: getIsNotable(tag, options),
    attributes,
  }
}

function getTextContent(element: HTMLElement, preference: Preferences) {
  if (preference === `attributes`) {
    return null
  }

  const childNodes = element.childNodes

  if (childNodes.length === 1 && childNodes[0].nodeType === Node.TEXT_NODE) {
    return element.textContent
  }

  return null
}

function getIsNotable(tag: string, options: Options) {
  if (options.inclusions.notableTags.includes(tag)) {
    return true
  }

  return false
}

function getAttributes(
  element: HTMLElement,
  options: Options,
  preference: Preferences
) {
  if (preference === `text`) {
    return null
  }

  return options.inclusions.attributes.reduce<AttributesMap>(
    (acc, attribute) => {
      const att = element.getAttribute(attribute)

      if (att) {
        const obj = acc || {}

        return {
          ...obj,
          [attribute]: element.getAttribute(attribute),
        }
      }

      return acc
    },
    null
  )
}
