import {
  BooleanField,
  Datagrid,
  DateField,
  NumberField,
  ReferenceManyField,
  Show,
  TabbedShowLayout,
  TextField,
} from 'react-admin'
import * as React from 'react'
import { CreateRelatedTodoItemButton } from '@/components/Persons/PersonEdit'

export const PersonShow = ({ properties }) => (
  <Show>
    <TabbedShowLayout>
      <TabbedShowLayout.Tab label='Person'>
        <TextField source={properties.person.name} />
        <DateField source={properties.person.createdAt} showTime={true} />
        <DateField source={properties.person.updatedAt} showTime={true} />
        <TextField source='id' />
      </TabbedShowLayout.Tab>
      <TabbedShowLayout.Tab label='Todo items'>
        <ReferenceManyField reference='todoitems' target={properties.todoitem.userId}>
          <Datagrid>
            <TextField source={properties.todoitem.name} />
            <BooleanField source={properties.todoitem.isComplete} />
            <DateField source={properties.todoitem.createdAt} showTime={true} />
            <DateField source={properties.todoitem.updatedAt} showTime={true} />
            <NumberField source='id' sortable={false} />
          </Datagrid>
        </ReferenceManyField>
        <CreateRelatedTodoItemButton userId={properties.todoitem.userId} />
      </TabbedShowLayout.Tab>
    </TabbedShowLayout>
  </Show>
)
