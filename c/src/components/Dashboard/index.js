import { Card, CardContent, CardHeader, Link } from '@mui/material'

export default function Dashboard() {
  const letterAlink = 'https://github.com/willianantunes/a-b-c-apps/tree/main/a'
  const letterBlink = 'https://github.com/willianantunes/a-b-c-apps/tree/main/b'
  const ndrfLink = 'https://github.com/juntossomosmais/NDjango.RestFramework'
  const drfLink = 'https://github.com/encode/django-rest-framework'
  return (
    <Card>
      <CardHeader title='Admin fully integrated with NDjango REST Framework (C#) and Django Rest Framework (Python)' />
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
      <CardContent>
        The backend application{' '}
        <Link href={letterBlink} target='_blank'>
          Letter B
        </Link>{' '}
        uses{' '}
        <Link href={drfLink} target='_blank'>
          Django Rest Framework.
        </Link>{' '}
        It follows the same principle.
      </CardContent>
    </Card>
  )
}
