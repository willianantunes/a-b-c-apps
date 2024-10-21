import { translateFilter, translateSort, translatePaginationQuery } from './page-number-navigation'

describe('translateFilter', () => {
  it('should transform keys to PascalCase', () => {
    const testCases = [
      { input: { name: 'John' }, expected: { Name: 'John' } },
      { input: { age: 30 }, expected: { Age: 30 } },
      { input: { isActive: true }, expected: { IsActive: true } },
      { input: { tags: ['typescript', 'javascript'] }, expected: { Tags: ['typescript', 'javascript'] } },
      {
        input: { address: { city: 'New York', zip: '10001' } },
        expected: { Address: { city: 'New York', zip: '10001' } },
      },
      { input: { scores: [85, 90, 78] }, expected: { Scores: [85, 90, 78] } },
      { input: { createdAt: new Date() }, expected: { CreatedAt: new Date() } },
      {
        input: { metadata: { author: 'Jane Doe', length: 1200 } },
        expected: { Metadata: { author: 'Jane Doe', length: 1200 } },
      },
      {
        input: { preferences: { theme: 'dark', notifications: false } },
        expected: { Preferences: { theme: 'dark', notifications: false } },
      },
      { input: { id: 'abc123', status: 'pending' }, expected: { Id: 'abc123', Status: 'pending' } },
    ]

    testCases.forEach(({ input, expected }) => {
      expect(translateFilter(input)).toEqual(expected)
    })
  })
})

describe('translateSort', () => {
  it('should transform sort to PascalCase and add Sort or SortDesc prefix', () => {
    const testCases = [
      { input: { field: 'title', order: 'asc' }, expected: { Sort: 'Title' } },
      { input: { field: 'name', order: 'desc' }, expected: { SortDesc: 'Name' } },
      { input: { field: 'bigWig', order: 'asc' }, expected: { Sort: 'BigWig' } },
    ]

    testCases.forEach(({ input, expected }) => {
      expect(translateSort(input)).toEqual(expected)
    })
  })
})

describe('translatePaginationQuery', () => {
  it('should transform pagination parameters correctly', () => {
    const testCases = [
      { input: { page: 1, perPage: 5 }, expected: { page: 1, per_page: 5 } },
      { input: { page: 2, perPage: 10 }, expected: { page: 2, per_page: 10 } },
      { input: { page: 3, perPage: 15 }, expected: { page: 3, per_page: 15 } },
      { input: { page: 4, perPage: 20 }, expected: { page: 4, per_page: 20 } },
      { input: { page: 5, perPage: 25 }, expected: { page: 5, per_page: 25 } },
    ]

    testCases.forEach(({ input, expected }) => {
      expect(translatePaginationQuery(input.page, input.perPage)).toEqual(expected)
    })
  })
})
