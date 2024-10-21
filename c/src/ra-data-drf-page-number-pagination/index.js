import { stringify } from 'query-string'
import { fetchUtils } from 'ra-core'
import * as PageNumberPagination from './page-number-navigation'

export default (apiUrl, httpClient = fetchUtils.fetchJson) => ({
  getList: async (resource, params) => {
    // Translate the query parameters to the format PageNumberPagination expects
    const query = {
      ...PageNumberPagination.translateFilter(params.filter),
      ...PageNumberPagination.translatePaginationQuery(params.pagination),
      ...PageNumberPagination.translateSort(params.sort),
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
  getManyReference: (resource, params) => {
    console.debug('getManyReference has been called', JSON.stringify(params))
    const { page, perPage } = params.pagination
    const { field, order } = params.sort

    const rangeStart = (page - 1) * perPage
    const rangeEnd = page * perPage - 1

    const query = {
      sort: JSON.stringify([field, order]),
      range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
      filter: JSON.stringify({
        ...params.filter,
        [params.target]: params.id,
      }),
    }
    const url = `${apiUrl}/${resource}?${stringify(query)}`
    const options =
      countHeader === 'Content-Range'
        ? {
            headers: new Headers({
              Range: `${resource}=${rangeStart}-${rangeEnd}`,
            }),
            signal: params?.signal,
          }
        : { signal: params?.signal }

    return httpClient(url, options).then(({ headers, json }) => {
      if (!headers.has(countHeader)) {
        throw new Error(
          `The ${countHeader} header is missing in the HTTP Response. The simple REST data provider expects responses for lists of resources to contain this header with the total number of results to build the pagination. If you are using CORS, did you declare ${countHeader} in the Access-Control-Expose-Headers header?`
        )
      }
      return {
        data: json,
        total:
          countHeader === 'Content-Range'
            ? parseInt(headers.get('content-range').split('/').pop(), 10)
            : parseInt(headers.get(countHeader.toLowerCase())),
      }
    })
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
