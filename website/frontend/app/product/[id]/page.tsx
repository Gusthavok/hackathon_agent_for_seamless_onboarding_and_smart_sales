'use client'

import { notFound } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { Product } from '@/types/Product'
import { useCart } from '@/contexts/CartContext'
import { Button } from "@/components/ui/button"
import { products_test } from "@/fake_data/test1"

const products: Product[] = products_test


export default function ProductPage({ params }: { params: { id: string } }) {
  const { addToCart } = useCart()
  const product = products.find(p => p.parent_asin === params.id)

  if (!product) {
    notFound()
  }

  return (
    <div className="container mx-auto px-4 py-8 overflow-auto">
      <Link href="/" className="text-blue-500 hover:underline mb-4 inline-block">&larr; Retour aux Produits</Link>
      <div className="flex flex-col md:flex-row gap-8">
        <div className="md:w-1/2 relative h-[400px]">
          <Image 
            src={product.images[0].large} 
            alt={product.title} 
            fill
            className="object-cover rounded-lg shadow-md"
          />
        </div>
        <div className="md:w-1/2">
          <h1 className="text-3xl font-bold mb-4">{product.title}</h1>
          <p className="text-xl text-gray-600 mb-4">{product.price.toFixed(2)} $</p>
          <div className="flex items-center mb-4">
            <span className="text-yellow-500">★</span>
            <span className="ml-1 text-sm text-gray-600">{product.average_rating.toFixed(1)} ({product.rating_number} avis)</span>
          </div>
          <h2 className="text-xl font-semibold mb-2">Caractéristiques :</h2>
          <ul className="list-disc pl-5 mb-4">
            {product.features.map((feature, index) => (
              <li key={index} className="text-gray-700">{feature}</li>
            ))}
          </ul>
          <h2 className="text-xl font-semibold mb-2">Description :</h2>
          {product.description.map((desc, index) => (
            <p key={index} className="text-gray-700 mb-2">{desc}</p>
          ))}
          <Button onClick={() => addToCart(product)} className="mt-4">
            Ajouter au panier
          </Button>
        </div>
      </div>
    </div>
  )
}

