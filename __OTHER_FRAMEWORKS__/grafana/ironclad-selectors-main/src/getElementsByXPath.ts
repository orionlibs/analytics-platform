export function getElementsByXPath(path: string): HTMLElement[] {
  if (!path) {
    return []
  }

  const evaluator = new XPathEvaluator()
  const result = evaluator.evaluate(
    path,
    document.documentElement,
    null,
    XPathResult.ORDERED_NODE_ITERATOR_TYPE,
    null
  )
  const nodes: Node[] = []
  let node = result.iterateNext()

  while (node) {
    nodes.push(node)
    node = result.iterateNext()
  }

  return nodes.filter(isHTMLElement)
}

function isHTMLElement(node: Node): node is HTMLElement {
  return node instanceof HTMLElement
}
