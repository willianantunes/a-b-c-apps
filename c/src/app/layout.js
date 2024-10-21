export const metadata = {
  title: 'Application C',
  description: 'React-Admin for the Application A',
}

export default function RootLayout({ children }) {
  return (
    <html lang='en'>
      <body>{children}</body>
    </html>
  )
}
