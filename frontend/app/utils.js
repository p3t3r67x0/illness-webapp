export const groupBy = (items, param) => {
  return items.reduce((a, b) => {
    ;(a[b[param]] = a[b[param]] || []).push(b)

    return a
  }, {})
};
