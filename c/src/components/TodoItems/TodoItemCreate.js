import * as React from 'react'
import {
  CreateButton,
  Create,
  required,
  SimpleForm,
  TextInput,
  BooleanInput,
  useRecordContext,
  ReferenceField,
} from 'react-admin'

// const CreateRelatedPersonButton = () => {
//   const record = useRecordContext()
//   return <CreateButton resource='comments' state={{ record: { post_id: record.id } }} />
// }

export const TodoItemCreate = () => (
  <Create redirect='show'>
    <SimpleForm>
      <TextInput source='name' validate={[required()]} />
      <BooleanInput source='isComplete' validate={[required()]} />
      <ReferenceField reference='persons' source='userId' />
    </SimpleForm>
  </Create>
)
