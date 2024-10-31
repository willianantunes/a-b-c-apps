import dynamic from 'next/dynamic'

const AdminApp = dynamic(() => import('@/components/AdminApp'), { ssr: false })

const Home = () => <AdminApp />

export default Home
