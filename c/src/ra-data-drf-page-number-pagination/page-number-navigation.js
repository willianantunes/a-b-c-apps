const translatePaginationQuery = ({ page, perPage }) => {
  return {
    page: page,
    per_page: perPage,
  }
}

const translateFilter = (filter) => {
  const transformedFilter = {}
  for (const key in filter) {
    if (filter.hasOwnProperty(key)) {
      const keyAsPascalCase = key.charAt(0).toUpperCase() + key.slice(1)
      transformedFilter[keyAsPascalCase] = filter[key]
    }
  }
  return transformedFilter
}

const translateSort = (sort) => {
  const { field, order } = sort
  const fieldAsPascalCase = field.charAt(0).toUpperCase() + field.slice(1)
  const key = `${order.toUpperCase() === 'ASC' ? 'Sort' : 'SortDesc'}`
  return {
    [key]: fieldAsPascalCase,
  }
}

export { translatePaginationQuery, translateFilter, translateSort }
