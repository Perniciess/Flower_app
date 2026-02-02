import Link from "next/link";

export function Footer() {
    return (
        <footer className="mt-auto bg-[#326964] text-white">
            <div className="border-b border-white/20 px-4 py-8 text-center">
                <p className="text-lg">
                    Бережная круглосуточная доставка
                    {" "}
                    <br />
                    свежих цветов по Челябинску
                </p>
                <Link href="" className="text-gray-200 underline">Наши адреса</Link>
            </div>
            <div className="border-b border-white/20 px-4 py-16">
                <div className="mx-auto grid max-w-6xl grid-cols-5 gap-8">
                    <div>
                        <h3 className="mb-4 font-semibold">Цветы</h3>
                        <ul className="space-y-2 text-sm text-white/80">
                            <li><Link href="" className="">Каталог цветов</Link></li>
                            <li><Link href="" className="">Конструктор букетов</Link></li>
                            <li><Link href="" className="">Розы</Link></li>
                            <li><Link href="" className="">Советы</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="mb-4 font-semibold">Поводы</h3>
                        <ul className="space-y-2 text-sm text-white/80">
                            <li><Link href="" className="">День Рождения и Юбилей</Link></li>
                            <li><Link href="" className="">Свадьба</Link></li>
                            <li><Link href="" className="">Извинения</Link></li>
                            <li><Link href="" className="">Выписка</Link></li>
                            <li><Link href="" className="">Люблю</Link></li>
                            <li><Link href="" className="">Зима</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="mb-4 font-semibold">Подарки</h3>
                        <ul className="space-y-2 text-sm text-white/80">
                            <li><Link href="" className="">Подарочные сертификаты</Link></li>
                            <li><Link href="" className="">Игрушки</Link></li>
                            <li><Link href="" className="">Шары</Link></li>
                            <li><Link href="" className="">Конфенты</Link></li>
                            <li><Link href="" className="">Декор</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="mb-4 font-semibold">О компании</h3>
                        <ul className="space-y-2 text-sm text-white/80">
                            <li><Link href="" className="">Контакты</Link></li>
                            <li><Link href="" className="">Бонусная программа</Link></li>
                            <li><Link href="" className="">Вакансии</Link></li>
                            <li><Link href="" className="">Доставка и оплата</Link></li>
                            <li><Link href="" className="">Условия возврата</Link></li>
                            <li><Link href="" className="">Публичный договор-оферта</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="mb-4 font-semibold">Контакты</h3>
                        <ul className="space-y-2 text-sm text-white/80">
                            <li>
                                <a href="tel:89007707021" className="text-2xl  font-bold">8 900 770 7021</a>
                                <p className="text-s text-white/60">Звонок бесплатный</p>
                            </li>
                            <li><a href="mailto:sales@kupibuket74.ru" className="text-2xl ">sales@kupibuket74.ru</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div className="px-4 py-4 text-center text-sm text-white/70">
                <p>
                    &copy;
                    {new Date().getFullYear()}
                    {" "}
                    ЦВЕТОПТОРГ • ИП Соколова Т.С. • Публичный договор оферты • Политика Конфиденциальности • Условия использования
                </p>
            </div>
        </footer>
    );
}
