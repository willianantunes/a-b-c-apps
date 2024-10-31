import { Card, CardContent, CardHeader, Link } from '@mui/material'

export default function Dashboard() {
  const letterAlink = 'https://github.com/willianantunes/a-b-c-apps/tree/main/a'
  const ndrfLink = 'https://github.com/juntossomosmais/NDjango.RestFramework'
  return (
    <Card>
      <CardHeader title='Admin fully integrated with NDjango REST Framework' />
      <CardContent>
        Check out the backend application{' '}
        <Link href={letterAlink} target='_blank'>
          Letter A
        </Link>{' '}
        that uses{' '}
        <Link href={ndrfLink} target='_blank'>
          NDjango.RestFramework
        </Link>{' '}
        and understand how it works.
      </CardContent>
    </Card>
  )
}
