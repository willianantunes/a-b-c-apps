import { stringify } from 'query-string'
import { fetchUtils } from 'ra-core'
import * as NDjangoRestFrameworkPagination from './ndjango-rest-framework-pagination'

export default (apiUrl, httpClient = fetchUtils.fetchJson) => ({
  getList: async (resource, params) => {
    console.debug('getList has been called', JSON.stringify(params))
    // Translate the query parameters to the format NDjangoRestFrameworkPagination expects
    const query = {
      ...NDjangoRestFrameworkPagination.translateFilter(params.filter),
      ...NDjangoRestFrameworkPagination.translatePaginationQuery(params.pagination),
      ...NDjangoRestFrameworkPagination.translateSort(params.sort),
    }
    console.debug('query', JSON.stringify(query))
    const url = `${apiUrl}/${resource}?${stringify(query)}`
    const options = { signal: params?.signal }
    try {
      // Call the API (check out https://github.com/juntossomosmais/NDjango.RestFramework)
      const { json } = await httpClient(url, options)
      // Use `Partial Pagination`. Check out https://marmelab.com/react-admin/DataProviderWriting.html#partial-pagination
      const hasPreviousPage = json.hasOwnProperty('previous') && json['previous'] !== ''
      const hasNextPage = json.hasOwnProperty('next') && json['next'] !== ''
      const hasCount = json.hasOwnProperty('count')
      const dataToBeReturned = {
        data: json.results,
        pageInfo: {
          hasPreviousPage: hasPreviousPage,
          hasNextPage: hasNextPage,
        },
      }
      if (hasCount) {
        dataToBeReturned['total'] = json.count
      }
      return dataToBeReturned
    } catch (error) {
      if (error.status === 404) {
        console.log('Returning empty data because of 404')
        return { data: [], total: 0, pageInfo: { hasPreviousPage: false, hasNextPage: false } }
      }
      throw error
    }
  },
  getOne: (resource, params) => {
    console.debug('getOne has been called', JSON.stringify(params))
    return httpClient(`${apiUrl}/${resource}/${encodeURIComponent(params.id)}`, {
      signal: params?.signal,
    }).then(({ json }) => ({
      data: json,
    }))
  },
  getMany: (resource, params) => {
    console.debug('getMany has been called', JSON.stringify(params))
    const query = { ids: params.ids }
    const url = `${apiUrl}/${resource}?${stringify(query)}`
    return httpClient(url, { signal: params?.signal }).then(({ json }) => ({
      data: json.results,
    }))
  },
  getManyReference: async (resource, params) => {
    console.debug('getManyReference has been called', JSON.stringify(params))
    // Translate the query parameters to the format NDjangoRestFrameworkPagination expects
    const query = {
      ...NDjangoRestFrameworkPagination.translateFilter(params.filter),
      ...NDjangoRestFrameworkPagination.translatePaginationQuery(params.pagination),
      ...NDjangoRestFrameworkPagination.translateSort(params.sort),
      [params.target]: params.id,
    }
    const url = `${apiUrl}/${resource}?${stringify(query)}`
    const options = { signal: params?.signal }
    try {
      // Call the API (check out https://github.com/juntossomosmais/NDjango.RestFramework)
      const { json } = await httpClient(url, options)
      // Use `Partial Pagination`. Check out https://marmelab.com/react-admin/DataProviderWriting.html#partial-pagination
      const hasPreviousPage = json.hasOwnProperty('previous') && json['previous'] !== ''
      const hasNextPage = json.hasOwnProperty('next') && json['next'] !== ''
      const hasCount = json.hasOwnProperty('count')
      const dataToBeReturned = {
        data: json.results,
        pageInfo: {
          hasPreviousPage: hasPreviousPage,
          hasNextPage: hasNextPage,
        },
      }
      if (hasCount) {
        dataToBeReturned['total'] = json.count
      }
      return dataToBeReturned
    } catch (error) {
      if (error.status === 404) {
        console.log('Returning empty data because of 404')
        return { data: [], total: 0, pageInfo: { hasPreviousPage: false, hasNextPage: false } }
      }
      throw error
    }
  },
  update: (resource, params) =>
    httpClient(`${apiUrl}/${resource}/${encodeURIComponent(params.id)}`, {
      method: 'PUT',
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json })),
  updateMany: (resource, params) =>
    Promise.all(
      params.ids.map((id) =>
        httpClient(`${apiUrl}/${resource}/${encodeURIComponent(id)}`, {
          method: 'PUT',
          body: JSON.stringify(params.data),
        })
      )
    ).then((responses) => ({
      data: responses.map(({ json }) => json.id),
    })),
  create: (resource, params) =>
    httpClient(`${apiUrl}/${resource}`, {
      method: 'POST',
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json })),
  delete: (resource, params) =>
    httpClient(`${apiUrl}/${resource}/${encodeURIComponent(params.id)}`, {
      method: 'DELETE',
      headers: new Headers({
        'Content-Type': 'text/plain',
      }),
    }).then(({ json }) => ({ data: json })),
  deleteMany: (resource, params) =>
    Promise.all(
      params.ids.map((id) =>
        httpClient(`${apiUrl}/${resource}/${encodeURIComponent(id)}`, {
          method: 'DELETE',
          headers: new Headers({
            'Content-Type': 'text/plain',
          }),
        })
      )
    ).then((responses) => ({
      data: responses.map(({ json }) => json.id),
    })),
})
