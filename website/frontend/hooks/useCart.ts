import { useState, useEffect } from 'react'
import { Product } from '@/types/Product'

interface CartItem extends Product {
  quantity: number
}

export function useCart() {
  const [cart, setCart] = useState<CartItem[]>([])

  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      setCart(JSON.parse(savedCart))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart))
  }, [cart])

  const addToCart = (product: Product) => {
    setCart(currentCart => {
      const existingItem = currentCart.find(item => item.id === product.id)
      if (existingItem) {
        return currentCart.map(item =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        )
      }
      return [...currentCart, { ...product, quantity: 1 }]
    })
  }

  const removeFromCart = (productId: number) => {
    setCart(currentCart => currentCart.filter(item => item.id !== productId))
  }

  const updateQuantity = (productId: number, quantity: number) => {
    setCart(currentCart =>
      currentCart.map(item =>
        item.id === productId ? { ...item, quantity: Math.max(1, quantity) } : item
      )
    )
  }

  return { cart, addToCart, removeFromCart, updateQuantity }
}

