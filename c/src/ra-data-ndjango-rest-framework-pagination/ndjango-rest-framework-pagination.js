const translatePaginationQuery = ({ page, perPage }) => {
  return {
    page: page,
    page_size: perPage,
  }
}

const translateFilter = (filter) => {
  const transformedFilter = {}
  for (const key in filter) {
    if (filter.hasOwnProperty(key)) {
      const isSpecialKey = key === '_interceptChangeToSearch' // Check out `PersonList.js` file
      if (isSpecialKey) {
        transformedFilter['search'] = `%${filter[key]}%`
      }
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
