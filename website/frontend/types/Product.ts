export interface Product {
  id: number
  
  main_category: string
  title: string
  average_rating: number
  rating_number: number
  features: string[]
  description: string[]
  price: number
  images: {
    hi_res: string
    thumb: string
    large: string
    variant: string
  }[]
  videos: { title: string; url: string }[]
  store: string
  categories: string[]

  parent_asin: string
  bought_together: string[] | null
}

