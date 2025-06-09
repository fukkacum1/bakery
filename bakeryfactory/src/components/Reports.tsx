import { observer } from 'mobx-react-lite';
import bakeryStore from '../stores/BakeryStore';

const Reports = observer(() => {
  const { total_price, max_profit, invalid_products, max_ingredients } = bakeryStore.reports;

  return (
    <div className="bg-white shadow-md rounded p-6">
      <h2 className="text-xl font-bold mb-4">Отчёты</h2>
      <div className="space-y-4">
        <div>
          <p className="text-gray-700">Общая цена: <span className="font-semibold">{total_price || 0} руб</span></p>
        </div>
        <div>
          <p className="text-gray-700">
            Максимальная прибыль: <span className="font-semibold">{max_profit?.name || 'N/A'} - {max_profit?.profit || 0} руб</span>
          </p>
        </div>
        <div>
          <p className="text-gray-700">Просроченные изделия:</p>
          <ul className="list-disc list-inside">
            {invalid_products && invalid_products.length > 0 ? (
              invalid_products.map((product, index) => (
                <li key={index} className="text-gray-600">
                  {product.name || 'Без названия'} (Вес: {product.weight || 0} г)
                </li>
              ))
            ) : (
              <li className="text-gray-600">Нет просроченных изделий</li>
            )}
          </ul>
        </div>
        <div>
          <p className="text-gray-700">
            Самый используемый ингредиент: <span className="font-semibold">{max_ingredients?.name || 'N/A'} - {max_ingredients?.ingredient_count || 0} ед</span>
          </p>
        </div>
      </div>
    </div>
  );
});

export default Reports;