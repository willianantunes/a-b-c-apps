'use client'
import { Admin, Resource } from 'react-admin'
import PostIcon from '@mui/icons-material/Book'
import UserIcon from '@mui/icons-material/Group'
import customDataProvider from '@/ra-data-ndjango-rest-framework-pagination'
import { PersonCreate } from '@/components/Persons/PersonCreate'
import { TodoItemCreate } from '@/components/TodoItems/TodoItemCreate'
import { PersonList } from '@/components/Persons/PersonList'
import { TodoItemList } from '@/components/TodoItems/TodoItemList'
import { PersonEdit } from '@/components/Persons/PersonEdit'
import { PersonShow } from '@/components/Persons/PersonShow'
import { TodoItemShow } from '@/components/TodoItems/TodoItemShow'
import { Dashboard } from '@/components/Dashboard'
import { TodoItemEdit } from '@/components/TodoItems/TodoItemEdit'

const dataProvider = customDataProvider('http://localhost:8000/api/v1')

export default function Index() {
  return (
    <Admin dataProvider={dataProvider} dashboard={Dashboard}>
      <Resource
        name='persons'
        create={PersonCreate}
        list={PersonList}
        edit={PersonEdit}
        show={PersonShow}
        icon={UserIcon}
        recordRepresentation='name'
      />
      <Resource
        name='todoitems'
        create={TodoItemCreate}
        list={TodoItemList}
        edit={TodoItemEdit}
        show={TodoItemShow}
        icon={PostIcon}
      />
    </Admin>
  )
}
