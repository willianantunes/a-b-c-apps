import {
  AutocompleteInput,
  BooleanInput,
  DateInput,
  Edit,
  ReferenceInput,
  required,
  SimpleForm,
  TextInput,
} from 'react-admin'
import * as React from 'react'

export const TodoItemEdit = ({ properties }) => {
  // https://marmelab.com/react-admin/ReferenceInput.html#customizing-the-filter-query
  const filterToQuery = (searchText) => ({ search: `%${searchText}%` })

  return (
    <Edit>
      <SimpleForm>
        <TextInput source={properties.name} />
        <BooleanInput source={properties.isComplete} />
        <DateInput source={properties.createdAt} InputProps={{ disabled: true }} />
        <DateInput source={properties.updatedAt} InputProps={{ disabled: true }} />
        <ReferenceInput source={properties.userId} reference='persons'>
          <AutocompleteInput filterToQuery={filterToQuery} validate={required()} />
        </ReferenceInput>
        <TextInput source='id' InputProps={{ disabled: true }} />
      </SimpleForm>
    </Edit>
  )
}
