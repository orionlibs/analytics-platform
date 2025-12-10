import { FAIL_CRITERIA } from "consts"
import { getElementsByXPath } from "getElementsByXPath"
import { Options } from "types"

export function checkCriteria(xPathSelector: string, options: Options) {
  const elements = getElementsByXPath(xPathSelector)
  const failCriteria = checkFailCriteria(elements, options)

  if (failCriteria) {
    return failCriteria
  }

  return null
}

function checkFailCriteria(elements: HTMLElement[], options: Options) {
  if (elements.length === 0) {
    return {
      type: FAIL_CRITERIA.NO_ELEMENTS_FOUND,
      meta: null,
    }
  }

  if (elements.length > 1) {
    return {
      type: FAIL_CRITERIA.MULTIPLE_ELEMENTS_FOUND,
      meta: null,
    }
  }

  return null
}
