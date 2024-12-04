import {
  BooleanField,
  CreateButton,
  Datagrid,
  DateField,
  DateInput,
  Edit,
  NumberField,
  ReferenceManyField,
  TabbedForm,
  TextField,
  TextInput,
  useRecordContext,
} from 'react-admin'
import * as React from 'react'

export const CreateRelatedTodoItemButton = ({ userId }) => {
  const user = useRecordContext()
  return <CreateButton resource='todoitems' state={{ record: { [userId]: user.id } }} />
}

export const PersonEdit = ({ properties }) => {
  return (
    <Edit>
      <TabbedForm>
        <TabbedForm.Tab label='User'>
          <TextInput source={properties.person.name} />
          <DateInput source={properties.person.createdAt} InputProps={{ disabled: true }} />
          <DateInput source={properties.person.updatedAt} InputProps={{ disabled: true }} />
          <TextInput source='id' InputProps={{ disabled: true }} />
        </TabbedForm.Tab>
        <TabbedForm.Tab label='Todo items'>
          <ReferenceManyField reference='todoitems' target={properties.todoitem.userId}>
            <Datagrid>
              <TextField source={properties.todoitem.name} />
              <BooleanField source={properties.todoitem.isComplete} />
              <DateField source={properties.todoitem.createdAt} showTime={true} />
              <DateField source={properties.todoitem.updatedAt} showTime={true} />
              <NumberField source='id' />
            </Datagrid>
          </ReferenceManyField>
          <CreateRelatedTodoItemButton userId={properties.todoitem.userId} />
        </TabbedForm.Tab>
      </TabbedForm>
    </Edit>
  )
}
