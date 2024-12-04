import { Datagrid, DateField, List, TextField, NumberField, TextInput } from 'react-admin'

const personFilters = [
  // `_interceptChangeToSearch` is a special source.
  // Check the implementation in `ra-data-ndjango-rest-framework-pagination` or `ra-data-django-rest-framework-pagination` for more details.
  <TextInput source='_interceptChangeToSearch' label='Search by name' alwaysOn />,
]

export const PersonList = ({ properties }) => (
  <List filters={personFilters} sort={{ field: properties.createdAt, order: 'DESC' }}>
    <Datagrid>
      <NumberField source='id' sortable={false} />
      <TextField source={properties.name} />
      <DateField source={properties.createdAt} showTime={true} />
      <DateField source={properties.updatedAt} showTime={true} />
    </Datagrid>
  </List>
)
