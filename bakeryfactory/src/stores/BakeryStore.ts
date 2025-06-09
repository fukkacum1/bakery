import { makeAutoObservable } from 'mobx';

interface Bakery {
  id: number;
  name?: string;
}

interface Product {
  id?: number;
  name?: string;
  weight?: number;
  shelf_life?: number;
  price?: number;
  production_volume?: number;
  ingredients?: number[];
}

interface Ingredient {
  id: number;
  name: string;
}

interface Report {
  total_price?: number;
  max_profit?: { name: string; profit: number };
  invalid_products?: Product[];
  max_ingredients?: { name: string; ingredient_count: number };
}

class BakeryStore {
  bakeries: Bakery[] = [];
  selectedBakeryId: string | null = null; // Изменил с number на string
  products: Product[] = [];
  ingredients: Ingredient[] = [];
  reports: Report = {};
  loading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  setLoading(loading: boolean) {
    this.loading = loading;
  }

  setError(error: string | null) {
    this.error = error;
  }

  setSelectedBakery(id: string | null) { // Изменил тип с number на string
    this.selectedBakeryId = id;
  }

  async fetchBakeries() {
    this.setLoading(true);
    try {
      this.bakeries = [
        { id: 1, name: 'Хлебозавод №1' },
        { id: 2, name: 'Хлебозавод №2' },
        { id: 3, name: 'Хлебозавод №3' },
      ];
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка загрузки хлебозаводов');
    } finally {
      this.setLoading(false);
    }
  }

  async fetchProducts() {
    this.setLoading(true);
    try {
      this.products = [
        { id: 1, name: 'Батон', weight: 400, shelf_life: 72, price: 50, production_volume: 100, ingredients: [1, 2] },
        { id: 2, name: 'Круассан', weight: 80, shelf_life: 24, price: 120, production_volume: 50, ingredients: [1, 3] },
      ];
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка загрузки продуктов');
    } finally {
      this.setLoading(false);
    }
  }

  async fetchIngredients() {
    this.setLoading(true);
    try {
      this.ingredients = [
        { id: 1, name: 'Мука' },
        { id: 2, name: 'Соль' },
        { id: 3, name: 'Масло' },
      ];
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка загрузки ингредиентов');
    } finally {
      this.setLoading(false);
    }
  }

  async fetchReports() {
    this.setLoading(true);
    try {
      this.reports = {
        total_price: 5000,
        max_profit: { name: 'Батон', profit: 30 },
        invalid_products: [{ id: 3, name: 'Просрочка', weight: 300, shelf_life: 0, price: 0, production_volume: 0 }],
        max_ingredients: { name: 'Мука', ingredient_count: 100 },
      };
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка загрузки отчётов');
    } finally {
      this.setLoading(false);
    }
  }

  async addProduct(productData: Product) {
    this.setLoading(true);
    try {
      const newProduct: Product = {
        id: Date.now(), // Генерируем уникальный id
        ...productData,
      };
      this.products = [...this.products, newProduct];
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка добавления продукта');
    } finally {
      this.setLoading(false);
    }
  }

  async deleteProduct(productId: number) {
    this.setLoading(true);
    try {
      this.products = this.products.filter((p) => p.id !== productId);
      this.setError(null);
    } catch (err: any) {
      this.setError('Ошибка удаления продукта');
    } finally {
      this.setLoading(false);
    }
  }
}

const bakeryStore = new BakeryStore();
export default bakeryStore;