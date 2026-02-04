import Image from "next/image";
import { Button } from "@/shared/ui/components/button";

export function Hero() {
    return (
        <section className="relative aspect-[1440/707] w-full overflow-hidden rounded-b-2xl">
            <Image
                src="/images/flower_main.jpg"
                alt="Цветы"
                fill
                priority
                className="object-cover object-[center_62%]"
            />
            <div className="absolute inset-0 z-[5] bg-black/55" />
            <div className="relative z-10 flex h-full flex-col">
                <div className="absolute inset-0 z-10 -mt-[5px] flex flex-col items-center justify-center gap-[14px]">
                    <h1 className="text-center text-[48px] font-medium leading-[125%] text-white">
                        Цветы, которые
                        {" "}
                        <br />
                        {" "}
                        дарят эмоции
                    </h1>
                    <p className="text-center text-[20px] font-normal leading-[24px] text-white">
                        Мы создаём букеты, которые радуют, удивляют
                        <br />
                        и запоминаются. Свежие цветы, стильная
                        <br />
                        упаковка и быстрая доставка по Челябинску.
                    </p>
                    <Button variant="white_primary" className="mt-[5px] w-[249px]">Посмотреть каталог</Button>
                </div>
                <div className="absolute left-1/2 top-[87.7%] z-10 flex w-[1038px] -translate-x-1/2 items-center justify-center gap-[23px]">
                    <div className="flex items-center gap-4">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="48" height="48" fill="none" stroke="white" strokeWidth="16"><path d="M208 464h96v32h-96zm-16-48h128v32H192zM369.42 62.69C339.35 32.58 299.07 16 256 16A159.62 159.62 0 0 0 96 176c0 46.62 17.87 90.23 49 119.64l4.36 4.09C167.37 316.57 192 339.64 192 360v40h48V269.11L195.72 244 214 217.72 256 240l41.29-22.39 19.1 25.68-44.39 26V400h48v-40c0-19.88 24.36-42.93 42.15-59.77l4.91-4.66C399.08 265 416 223.61 416 176a159.16 159.16 0 0 0-46.58-113.31" /></svg>
                        <p className="text-[18px] text-white">
                            Собираем букет после
                            <br />
                            {" "}
                            вашего заказа
                        </p>
                    </div>
                    <div className="flex items-center gap-4">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="48" height="48" fill="none" stroke="white" strokeWidth="16"><path d="M208 464h96v32h-96zm-16-48h128v32H192zM369.42 62.69C339.35 32.58 299.07 16 256 16A159.62 159.62 0 0 0 96 176c0 46.62 17.87 90.23 49 119.64l4.36 4.09C167.37 316.57 192 339.64 192 360v40h48V269.11L195.72 244 214 217.72 256 240l41.29-22.39 19.1 25.68-44.39 26V400h48v-40c0-19.88 24.36-42.93 42.15-59.77l4.91-4.66C399.08 265 416 223.61 416 176a159.16 159.16 0 0 0-46.58-113.31" /></svg>
                        <p className="text-[18px] text-white">
                            Доставка за 60 минут,
                            <br />
                            {" "}
                            при необходимости
                        </p>
                    </div>
                    <div className="flex items-center gap-4">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="48" height="48" fill="none" stroke="white" strokeWidth="16"><path d="M208 464h96v32h-96zm-16-48h128v32H192zM369.42 62.69C339.35 32.58 299.07 16 256 16A159.62 159.62 0 0 0 96 176c0 46.62 17.87 90.23 49 119.64l4.36 4.09C167.37 316.57 192 339.64 192 360v40h48V269.11L195.72 244 214 217.72 256 240l41.29-22.39 19.1 25.68-44.39 26V400h48v-40c0-19.88 24.36-42.93 42.15-59.77l4.91-4.66C399.08 265 416 223.61 416 176a159.16 159.16 0 0 0-46.58-113.31" /></svg>
                        <p className="text-[18px] text-white">
                            Вы сами проектируете
                            <br />
                            {" "}
                            свой букет по вкусу
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}
