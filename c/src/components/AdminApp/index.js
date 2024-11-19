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
import { TodoItemEdit } from '@/components/TodoItems/TodoItemEdit'
import Dashboard from '@/components/Dashboard'
import { PUBLIC_LETTER_A_API } from '@/app/settings'
import { startOtelInstrumentation } from '@/otlp-browser'

const dataProvider = customDataProvider(PUBLIC_LETTER_A_API)

startOtelInstrumentation()

export default function AdminApp() {
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
