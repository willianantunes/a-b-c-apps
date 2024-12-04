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
        // https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
        transformedFilter['search'] = filter[key]
      }
    }
  }
  return transformedFilter
}

const translateSort = (sort) => {
  const { field, order } = sort
  return {
    ordering: `${order === 'ASC' ? '' : '-'}${field}`,
  }
}

export { translatePaginationQuery, translateFilter, translateSort }
