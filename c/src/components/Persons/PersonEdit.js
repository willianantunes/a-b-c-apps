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

export const CreateRelatedTodoItemButton = () => {
  const user = useRecordContext()
  return <CreateButton resource='todoitems' state={{ record: { userId: user.id } }} />
}

export const PersonEdit = () => {
  return (
    <Edit>
      <TabbedForm>
        <TabbedForm.Tab label='User'>
          <TextInput source='name' />
          <DateInput source='createdAt' InputProps={{ disabled: true }} />
          <DateInput source='updatedAt' InputProps={{ disabled: true }} />
          <TextInput source='id' InputProps={{ disabled: true }} />
        </TabbedForm.Tab>
        <TabbedForm.Tab label='Todo items'>
          <ReferenceManyField reference='todoitems' target='userId'>
            <Datagrid>
              <TextField source='name' />
              <BooleanField source='isComplete' />
              <DateField source='createdAt' showTime={true} />
              <DateField source='updatedAt' showTime={true} />
              <NumberField source='id' />
            </Datagrid>
          </ReferenceManyField>
          <CreateRelatedTodoItemButton />
        </TabbedForm.Tab>
      </TabbedForm>
    </Edit>
  )
}
