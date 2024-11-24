'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Product } from '@/types/Product'
import { useCart } from '@/contexts/CartContext'
import { Button } from "@/components/ui/button"
import { API_URL } from '@/app/api'
import { getFromLocalStorage } from '@/utils/localStorageHelper'; // Importer le helper pour localStorage

export default function ProductDisplay() {
  const { addToCart } = useCart()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true)

        // Récupérer le username du localStorage
        const username = getFromLocalStorage('username'); // Remplacer 'username' par la clé exacte

        // Ajouter le username dans les headers de la requête
        const response = await fetch(API_URL + '/api/products', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Username': username, // Ajouter le username dans les headers
          },
        })

        console.log('Response status:', response.status)  // Ajoutez ce log
        if (!response.ok) {
          throw new Error(`Erreur: ${response.statusText}`)
        }

        const data: Product[] = await response.json()
        console.log('Data fetched:', data)  // Ajoutez ce log
        setProducts(data)
      } catch (err: any) {
        console.error('Error:', err)  // Log plus détaillé pour l'erreur
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
  
    fetchProducts()
  }, []) // L'effet ne dépend de rien d'autre

  if (loading) {
    return <p className="text-center mt-10">Chargement des produits...</p>
  }

  if (error) {
    return <p className="text-center text-red-500 mt-10">Erreur: {error}</p>
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="flex justify-between items-center p-6">
        <h1 className="text-3xl font-bold">Nos Produits</h1>
        <Link href="/cart">
          <Button variant="outline">Voir le panier</Button>
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        {products.map((product) => (
          <div key={product.parent_asin} className="border rounded-lg p-3 shadow-sm flex flex-col">
            <Link href={`/product/${product.parent_asin}`} className="group">
              <div className="relative w-full h-48 mb-2">
                <Image 
                  src={product.images[0].large} 
                  alt={product.title} 
                  fill
                  className="object-cover rounded group-hover:opacity-80 transition-opacity"
                />
              </div>
              <h2 className="text-md font-semibold group-hover:text-blue-500 transition-colors">{product.title}</h2>
              <p className="text-gray-600 text-sm">{product.price.toFixed(2)} $</p>
              <div className="flex items-center mt-1">
                <span className="text-yellow-500">★</span>
                <span className="ml-1 text-sm text-gray-600">{product.average_rating.toFixed(1)} ({product.rating_number} avis)</span>
              </div>
            </Link>
            <Button 
              className="mt-2" 
              onClick={() => addToCart(product)}
            >
              Ajouter au panier
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}
