'use client'
import { Admin, EditGuesser, Resource, ShowGuesser } from 'react-admin'
import drfPageNumberPagination from '@/ra-data-drf-page-number-pagination'
import { PersonCreate } from '@/components/Persons/PersonCreate'
import { TodoItemCreate } from '@/components/TodoItems/TodoItemCreate'
import { PersonList } from '@/components/Persons/PersonList'
import { TodoitemList } from '@/components/TodoItems/TodoItemList'

const dataProvider = drfPageNumberPagination('http://localhost:8000/api/v1')

export default function Index() {
  return (
    <Admin dataProvider={dataProvider}>
      <Resource name='persons' create={PersonCreate} list={PersonList} edit={EditGuesser} show={ShowGuesser} />
      <Resource name='todoitems' create={TodoItemCreate} list={TodoitemList} edit={EditGuesser} show={ShowGuesser} />
    </Admin>
  )
}
