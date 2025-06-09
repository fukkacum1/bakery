import React from 'react';

const Header: React.FC = () => {
    return (
        <nav className="bg-blue-600 text-white p-4 shadow-md">
            <div className="container mx-auto flex justify-between items-center">
                <div className="text-xl font-bold">BreadFactory</div>
                <div className="space-x-4">
                    <a href="#" className="hover:underline focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1">Хлебозаводы</a>
                    <a href="#" className="hover:underline focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1">Изделия</a>
                    <a href="#" className="hover:underline focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1">Отчёты</a>
                    <a href="#" className="hover:underline focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1">Профиль</a>
                </div>
            </div>
        </nav>
    );
};

export default Header;