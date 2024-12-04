'use client'
import { Admin, Resource } from 'react-admin'
import PostIcon from '@mui/icons-material/Book'
import UserIcon from '@mui/icons-material/Group'
import customDataProviderNDrf from '@/ra-data-ndjango-rest-framework-pagination'
import customDataProviderDrf from '@/ra-data-django-rest-framework-pagination'
import { PersonCreate } from '@/components/Persons/PersonCreate'
import { TodoItemCreate } from '@/components/TodoItems/TodoItemCreate'
import { PersonList } from '@/components/Persons/PersonList'
import { TodoItemList } from '@/components/TodoItems/TodoItemList'
import { PersonEdit } from '@/components/Persons/PersonEdit'
import { PersonShow } from '@/components/Persons/PersonShow'
import { TodoItemShow } from '@/components/TodoItems/TodoItemShow'
import { TodoItemEdit } from '@/components/TodoItems/TodoItemEdit'
import Dashboard from '@/components/Dashboard'
import { startOtelInstrumentation } from '@/otlp-browser'
import { PUBLIC_LETTER_A_API } from '@/app/settings'
import { PUBLIC_LETTER_B_API } from '@/app/settings'

startOtelInstrumentation()

export default function AdminApp({ renderForApp }) {
  // Did it this way because I require `NEXT_PUBLIC_*` variables
  let dataProvider = null
  let models = {}
  if (renderForApp === 'a') {
    dataProvider = customDataProviderNDrf(PUBLIC_LETTER_A_API)
    models = {
      person: {
        name: 'name',
        createdAt: 'createdAt',
        updatedAt: 'updatedAt',
      },
      todoitem: {
        name: 'name',
        createdAt: 'createdAt',
        updatedAt: 'updatedAt',
        isComplete: 'isComplete',
        userId: 'userId',
      },
    }
  } else {
    dataProvider = customDataProviderDrf(PUBLIC_LETTER_B_API)
    models = {
      person: {
        name: 'name',
        createdAt: 'created_at',
        updatedAt: 'updated_at',
      },
      todoitem: {
        name: 'name',
        createdAt: 'created_at',
        updatedAt: 'updated_at',
        isComplete: 'is_complete',
        userId: 'person',
      },
    }
  }

  return (
    <Admin dataProvider={dataProvider} dashboard={Dashboard}>
      <Resource
        name='persons'
        create={<PersonCreate properties={models.person} />}
        list={<PersonList properties={models.person} />}
        edit={<PersonEdit properties={models} />}
        show={<PersonShow properties={models} />}
        icon={UserIcon}
        recordRepresentation='name'
      />
      <Resource
        name='todoitems'
        create={<TodoItemCreate properties={models.todoitem} />}
        list={<TodoItemList properties={models.todoitem} />}
        edit={<TodoItemEdit properties={models.todoitem} />}
        show={<TodoItemShow properties={models.todoitem} />}
        icon={PostIcon}
      />
    </Admin>
  )
}
