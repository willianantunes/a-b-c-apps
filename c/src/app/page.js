import Link from 'next/link'

export default function () {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
      }}
    >
      <h1>Choose which application you want to manage</h1>
      <h2>
        <Link href='/letter-a'>Letter A</Link>
      </h2>
      <h2>
        <Link href='/letter-b'>Letter B</Link>
      </h2>
    </div>
  )
}
