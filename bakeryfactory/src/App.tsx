
import { observer } from 'mobx-react-lite';
import { useEffect, useState } from 'react';
import bakeryStore from './stores/BakeryStore';
import AddProductForm from './components/AddProductForm';
import ProductList from './components/ProductList';
import Reports from './components/Reports';
import '../index.css';

const App = observer(() => {
  useEffect(() => {
    bakeryStore.fetchBakeries();
    bakeryStore.fetchProducts();
    bakeryStore.fetchIngredients();
    bakeryStore.fetchReports();
  }, []);

  const [selectedAction, setSelectedAction] = useState<string | null>(null);

  const handleQuickAction = (action: string) => {
    setSelectedAction(action);
    switch (action) {
      case 'view-products':
        console.log('Просмотр всех изделий');
        break;
      case 'max-profit':
        console.log('Найти самое прибыльное изделие');
        break;
      case 'expired-products':
        console.log('Изделия с нарушенным сроком');
        break;
      case 'sort-factories':
        console.log('Сортировка заводов по объему производства');
        break;
      case 'ingredients':
        console.log('Просмотр ингредиентов');
        break;
      case 'bakeries':
        console.log('Просмотр хлебозаводов');
        break;
    }
  };

  const handleSearch = (type: string, value: string) => {
    console.log(`Поиск ${type} по значению:`, value);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-50 p-6">
      <div className="max-w-[1200px] mx-auto">
        <header className="mb-8 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 bg-primary-500 rounded-full flex items-center justify-center">
              <span className="material-symbols-outlined text-white text-2xl">bakery_dining</span>
            </div>
            <h1 className="text-4xl font-bold text-gray-800">Система управления хлебозаводом</h1>
          </div>
          <p className="text-gray-600 text-lg">Управление изделиями, ингредиентами и хлебозаводами</p>
        </header>

        <nav className="mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                className="bg-gradient-to-r from-primary-500 to-primary-600 p-4 rounded-lg text-white hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
                onClick={() => handleQuickAction('view-products')}
              >
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-2xl">inventory</span>
                  <div>
                    <h3 className="font-semibold">Изделия</h3>
                    <p className="text-sm opacity-90">Управление продукцией</p>
                  </div>
                </div>
              </div>
              <div
                className="bg-gradient-to-r from-green-500 to-green-600 p-4 rounded-lg text-white hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
                onClick={() => handleQuickAction('ingredients')}
              >
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-2xl">restaurant</span>
                  <div>
                    <h3 className="font-semibold">Ингредиенты</h3>
                    <p className="text-sm opacity-90">Состав продуктов</p>
                  </div>
                </div>
              </div>
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-600 p-4 rounded-lg text-white hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
                onClick={() => handleQuickAction('bakeries')}
              >
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-2xl">factory</span>
                  <div>
                    <h3 className="font-semibold">Хлебозаводы</h3>
                    <p className="text-sm opacity-90">Производственные площадки</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <section className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary-500">add_circle</span>
              Добавить изделие
            </h2>
            <AddProductForm />
          </section>

          <section className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <span className="material-symbols-outlined text-green-500">analytics</span>
              Быстрые действия
            </h2>
            <div className="space-y-4">
              <button
                className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 px-4 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5 flex items-center gap-3"
                onClick={() => handleQuickAction('view-products')}
              >
                <span className="material-symbols-outlined">list_alt</span>
                <div className="text-left">
                  <div className="font-medium">Все изделия</div>
                  <div className="text-sm opacity-90">Просмотр всех продуктов</div>
                </div>
              </button>
              <button
                className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5 flex items-center gap-3"
                onClick={() => handleQuickAction('max-profit')}
              >
                <span className="material-symbols-outlined">trending_up</span>
                <div className="text-left">
                  <div className="font-medium">Максимальная прибыль</div>
                  <div className="text-sm opacity-90">Найти самое прибыльное изделие</div>
                </div>
              </button>
              <button
                className="w-full bg-gradient-to-r from-red-500 to-red-600 text-white py-3 px-4 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5 flex items-center gap-3"
                onClick={() => handleQuickAction('expired-products')}
              >
                <span className="material-symbols-outlined">warning</span>
                <div className="text-left">
                  <div className="font-medium">Просроченные</div>
                  <div className="text-sm opacity-90">Изделия с нарушенным сроком</div>
                </div>
              </button>
              <button
                className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-3 px-4 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5 flex items-center gap-3"
                onClick={() => handleQuickAction('sort-factories')}
              >
                <span className="material-symbols-outlined">sort</span>
                <div className="text-left">
                  <div className="font-medium">Сортировка заводов</div>
                  <div className="text-sm opacity-90">По объему производства</div>
                </div>
              </button>
            </div>
          </section>
        </main>

        <section className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-orange-500">search</span>
            Поиск и фильтрация
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Поиск по ID изделия</label>
              <div className="flex gap-2">
                <input
                  type="number"
                  id="productId"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  placeholder="ID изделия"
                  onChange={(e) => handleSearch('изделия', e.target.value)}
                />
                <button
                  className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors duration-200"
                  onClick={() => handleSearch('изделия', (document.getElementById('productId') as HTMLInputElement)?.value || '')}
                >
                  <span className="material-symbols-outlined">search</span>
                </button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">ID хлебозавода</label>
              <div className="flex gap-2">
                <input
                  type="number"
                  id="bakeryId"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  placeholder="ID завода"
                  onChange={(e) => handleSearch('хлебозавода', e.target.value)}
                />
                <button
                  className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors duration-200"
                  onClick={() => handleSearch('хлебозавода', (document.getElementById('bakeryId') as HTMLInputElement)?.value || '')}
                >
                  <span className="material-symbols-outlined">factory</span>
                </button>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Ингредиенты продукта</label>
              <div className="flex gap-2">
                <input
                  type="number"
                  id="ingredientProductId"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  placeholder="ID продукта"
                  onChange={(e) => handleSearch('ингредиентов', e.target.value)}
                />
                <button
                  className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors duration-200"
                  onClick={() => handleSearch('ингредиентов', (document.getElementById('ingredientProductId') as HTMLInputElement)?.value || '')}
                >
                  <span className="material-symbols-outlined">restaurant</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="material-symbols-outlined text-primary-500 text-xl">inventory</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">{bakeryStore.products.length}</span>
            </div>
            <h3 className="font-semibold text-gray-700 mb-1">Всего изделий</h3>
            <p className="text-sm text-gray-500">В системе</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <span className="material-symbols-outlined text-green-500 text-xl">restaurant</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">{bakeryStore.ingredients.length}</span>
            </div>
            <h3 className="font-semibold text-gray-700 mb-1">Ингредиентов</h3>
            <p className="text-sm text-gray-500">Уникальных</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="material-symbols-outlined text-blue-500 text-xl">factory</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">{bakeryStore.bakeries.length}</span>
            </div>
            <h3 className="font-semibold text-gray-700 mb-1">Хлебозаводов</h3>
            <p className="text-sm text-gray-500">Активных</p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <span className="material-symbols-outlined text-red-500 text-xl">warning</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">{bakeryStore.reports.invalid_products?.length || 0}</span>
            </div>
            <h3 className="font-semibold text-gray-700 mb-1">Нарушений</h3>
            <p className="text-sm text-gray-500">Срока годности</p>
          </div>
        </section>

        {selectedAction === 'view-products' && <ProductList />}
        {selectedAction === 'max-profit' && <Reports />}
        {selectedAction === 'expired-products' && <Reports />}
        {selectedAction === 'sort-factories' && <Reports />}

        <footer className="mt-12 text-center py-6 border-t border-gray-200">
          <p className="text-gray-500">© 2024 Система управления хлебозаводом. Все права защищены.</p>
        </footer>
      </div>
    </div>
  );
});

export default App;