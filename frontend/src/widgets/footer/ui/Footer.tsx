import Image from "next/image";
import Link from "next/link";
import { footerColumns } from "../config";

export function Footer() {
    return (
        <footer className="bg-[#326964] text-[18px] font-normal leading-none tracking-normal text-white">
            <div className="flex flex-col items-center border-b border-white/20 px-4 py-8">
                <Image src="/images/logo_white.png" alt="logo" width={90} height={70} className="mb-4" />
                <p className="text-center text-lg">
                    Бережная круглосуточная доставка
                    {" "}
                    <br />
                    {" "}
                    свежих цветов по Челябинску
                </p>
                <Link href="" className="text-gray-200 underline">Наши адреса</Link>
            </div>
            <div className="border-b border-white/20 py-16">
                <div className="mx-auto grid max-w-[1350px] grid-cols-[1fr_1fr_1fr_1fr_auto] gap-8 px-8">
                    {footerColumns.map((column) => (
                        <div key={column.title}>
                            <p className="mb-4 text-[20px] font-semibold">{column.title}</p>
                            <ul className="space-y-4 text-[#DADADA]">
                                {column.links.map((link) => (
                                    <li key={link.label}>
                                        <Link href={link.href}>{link.label}</Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                    <div>
                        <p className="mb-4 text-[20px] font-semibold">Контакты</p>
                        <ul className="space-y-4 text-white/80">
                            <li>
                                <a href="tel:89007707021" className="text-[28px]  font-semibold text-white">8 900 770 7021</a>
                                <p className="text-[18px] text-[#DADADA]">Звонок бесплатный</p>
                            </li>
                            <li>
                                <a href="mailto:sales@kupibuket74.ru" className="text-[20px] ">sales@kupibuket74.ru</a>
                            </li>
                            <li className="flex gap-2">
                                <a href="">
                                    <svg xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" viewBox="0 0 24 24" width="47" height="47" id="vk"><path fill="white" d="M15.07294,2H8.9375C3.33331,2,2,3.33331,2,8.92706V15.0625C2,20.66663,3.32294,22,8.92706,22H15.0625C20.66669,22,22,20.67706,22,15.07288V8.9375C22,3.33331,20.67706,2,15.07294,2Zm3.07287,14.27081H16.6875c-.55206,0-.71875-.44793-1.70831-1.4375-.86463-.83331-1.22919-.9375-1.44794-.9375-.30206,0-.38544.08332-.38544.5v1.3125c0,.35419-.11456.5625-1.04162.5625a5.69214,5.69214,0,0,1-4.44794-2.66668A11.62611,11.62611,0,0,1,5.35419,8.77081c0-.21875.08331-.41668.5-.41668H7.3125c.375,0,.51044.16668.65625.55212.70831,2.08331,1.91669,3.89581,2.40625,3.89581.1875,0,.27081-.08331.27081-.55206V10.10413c-.0625-.97913-.58331-1.0625-.58331-1.41663a.36008.36008,0,0,1,.375-.33337h2.29169c.3125,0,.41662.15625.41662.53125v2.89587c0,.3125.13544.41663.22919.41663.1875,0,.33331-.10413.67706-.44788a11.99877,11.99877,0,0,0,1.79169-2.97919.62818.62818,0,0,1,.63544-.41668H17.9375c.4375,0,.53125.21875.4375.53125A18.20507,18.20507,0,0,1,16.41669,12.25c-.15625.23956-.21875.36456,0,.64581.14581.21875.65625.64582,1,1.05207a6.48553,6.48553,0,0,1,1.22912,1.70837C18.77081,16.0625,18.5625,16.27081,18.14581,16.27081Z"></path></svg>
                                </a>
                                <a href="">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="47" height="47" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10s10-4.48 10-10S17.52 2 12 2m4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19c-.14.75-.42 1-.68 1.03c-.58.05-1.02-.38-1.58-.75c-.88-.58-1.38-.94-2.23-1.5c-.99-.65-.35-1.01.22-1.59c.15-.15 2.71-2.48 2.76-2.69a.2.2 0 0 0-.05-.18c-.06-.05-.14-.03-.21-.02c-.09.02-1.49.95-4.22 2.79c-.4.27-.76.41-1.08.4c-.36-.01-1.04-.2-1.55-.37c-.63-.2-1.12-.31-1.08-.66c.02-.18.27-.36.74-.55c2.92-1.27 4.86-2.11 5.83-2.51c2.78-1.16 3.35-1.36 3.73-1.36c.08 0 .27.02.39.12c.1.08.13.19.14.27c-.01.06.01.24 0 .38" /></svg>
                                </a>
                            </li>

                        </ul>
                    </div>
                </div>
            </div>
            <div className="px-4 py-4 text-center text-gray-300">
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
