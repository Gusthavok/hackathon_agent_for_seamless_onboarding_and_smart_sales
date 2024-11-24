'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useCart } from '@/contexts/CartContext'
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

export default function CartPage() {
  const { cart, removeFromCart, updateQuantity } = useCart()

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  return (
    <div className="container mx-auto px-4 py-8 overflow-auto">
      <h1 className="text-3xl font-bold mb-6">Votre Panier</h1>
        <p>Votre panier est vide.</p>
        <>
          <Table>
            <TableCaption>Liste des articles dans votre panier</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Produit</TableHead>
                <TableHead>Prix</TableHead>
                <TableHead>Quantité</TableHead>
                <TableHead>Total</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {cart.map((item) => (
                <TableRow key={item.parent_asin}>
                  <TableCell className="flex items-center space-x-2">
                    <div className="relative w-16 h-16">
                      <Image 
                        src={item.images[0].thumb} 
                        alt={item.title} 
                        fill
                        className="object-cover rounded"
                      />
                    </div>
                    <span>{item.title}</span>
                  </TableCell>
                  <TableCell>{item.price.toFixed(2)} $</TableCell>
                  <TableCell>
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) => updateQuantity(item.parent_asin, parseInt(e.target.value))}
                      className="w-16 p-1 border rounded"
                    />
                  </TableCell>
                  <TableCell>{(item.price * item.quantity).toFixed(2)} $</TableCell>
                  <TableCell>
                    <Button variant="destructive" onClick={() => removeFromCart(item.parent_asin)}>
                      Supprimer
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="mt-6 text-right">
            <p className="text-xl font-bold">Total: {total.toFixed(2)} $</p>
          </div>
          <div className="mt-6 flex justify-between">
            <Link href="/">
              <Button variant="outline">Continuer vos achats</Button>
            </Link>
            <Button>Passer à la caisse</Button>
          </div>
        </>
    </div>
  )
}

