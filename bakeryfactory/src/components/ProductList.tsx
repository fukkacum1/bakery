import { observer } from 'mobx-react-lite';
import bakeryStore from '../stores/BakeryStore';

const ProductList = observer(() => {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-bold mb-4">Список изделий</h2>
      {bakeryStore.products.length > 0 ? (
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-200">
              <th className="p-2 border">Название</th>
              <th className="p-2 border">Вес (г)</th>
              <th className="p-2 border">Срок годности (ч)</th>
              <th className="p-2 border">Цена (руб)</th>
              <th className="p-2 border">Объём производства</th>
            </tr>
          </thead>
          <tbody>
            {bakeryStore.products.map((product) => (
              <tr key={product.id} className="border-t">
                <td className="p-2 border">{product.name || 'Без названия'}</td>
                <td className="p-2 border">{product.weight || 0}</td>
                <td className="p-2 border">{product.shelf_life || 0}</td>
                <td className="p-2 border">{product.price || 0}</td>
                <td className="p-2 border">{product.production_volume || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="text-gray-500">Нет изделий для отображения.</p>
      )}
    </div>
  );
});

export default ProductList;