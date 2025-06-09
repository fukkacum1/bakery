import React, { useState } from 'react';
import bakeryStore from '../stores/BakeryStore';

interface ProductFormData {
  name: string;
  weight: number;
  shelf_life: number;
  price: number;
  production_volume: number; // Изменил с string на number
}

const AddProductForm: React.FC = () => {
  const [formData, setFormData] = useState<ProductFormData>({
    name: '',
    weight: 0,
    shelf_life: 0,
    price: 0,
    production_volume: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'weight' || name === 'shelf_life' || name === 'price' || name === 'production_volume' ? Number(value) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (bakeryStore.selectedBakeryId) {
      bakeryStore.addProduct(formData); // Убрал bakeryId, так как он не используется
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-100 p-6 rounded shadow-md mb-6">
      <h2 className="text-xl font-bold mb-4">Добавить изделие</h2>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Название
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="mt-1 p-2 border rounded w-full"
            required
          />
        </div>
        <div>
          <label htmlFor="weight" className="block text-sm font-medium text-gray-700">
            Вес (г)
          </label>
          <input
            type="number"
            id="weight"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            className="mt-1 p-2 border rounded w-full"
            required
          />
        </div>
        <div>
          <label htmlFor="shelf_life" className="block text-sm font-medium text-gray-700">
            Срок годности (ч)
          </label>
          <input
            type="number"
            id="shelf_life"
            name="shelf_life"
            value={formData.shelf_life}
            onChange={handleChange}
            className="mt-1 p-2 border rounded w-full"
            required
          />
        </div>
        <div>
          <label htmlFor="price" className="block text-sm font-medium text-gray-700">
            Цена (руб)
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            className="mt-1 p-2 border rounded w-full"
            required
          />
        </div>
        <div>
          <label htmlFor="production_volume" className="block text-sm font-medium text-gray-700">
            Объём производства
          </label>
          <input
            type="number"
            id="production_volume"
            name="production_volume"
            value={formData.production_volume}
            onChange={handleChange}
            className="mt-1 p-2 border rounded w-full"
            required
          />
        </div>
      </div>
      <button
        type="submit"
        className="mt-4 bg-blue-600 text-white p-2 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Добавить
      </button>
    </form>
  );
};

export default AddProductForm;