import * as React from 'react'
import {
  AutocompleteInput,
  BooleanInput,
  Create,
  getRecordFromLocation,
  ReferenceInput,
  required,
  SimpleForm,
  TextInput,
  useNotify,
  useRedirect,
} from 'react-admin'
import { useLocation } from 'react-router-dom'

export const TodoItemCreate = () => {
  const notify = useNotify()
  const redirect = useRedirect()
  const location = useLocation()

  // https://marmelab.com/blog/2023/10/12/react-admin-v4-advanced-recipes-creating-a-record-related-to-the-current-one.html
  const onSuccess = () => {
    // display a notification to confirm the creation
    notify('ra.notification.created')
    // get the initial values we set in the state earlier to know whether a userId was provided
    const record = getRecordFromLocation(location)
    let wasItCreatedFromTheUserEditPage = record && record.userId
    if (wasItCreatedFromTheUserEditPage) {
      // the record was created from the edit view of the user, redirect to it
      redirect(`/persons/${record.userId}`)
    } else {
      // redirect to the list of reviews
      redirect(`/todoitems`)
    }
  }

  // https://marmelab.com/react-admin/ReferenceInput.html#customizing-the-filter-query
  const filterToQuery = (searchText) => ({ search: `%${searchText}%` })

  return (
    <Create mutationOptions={{ onSuccess }}>
      <SimpleForm>
        <ReferenceInput source='userId' reference='persons'>
          <AutocompleteInput filterToQuery={filterToQuery} validate={required()} />
        </ReferenceInput>
        <TextInput source='name' validate={[required()]} />
        <BooleanInput source='isComplete' validate={[required()]} />
      </SimpleForm>
    </Create>
  )
}
