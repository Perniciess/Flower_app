import Image from "next/image";
import { Button } from "@/shared/ui/components/button";
import { CameraIcon, CarIcon, FlowerIcon } from "@/shared/ui/icons";

export function Hero() {
    return (
        <section className="relative aspect-[1440/707] min-h-dvh w-full overflow-hidden rounded-b-2xl">
            <Image
                src="/images/flower_main.jpg"
                alt="Цветы"
                fill
                priority
                className="object-cover object-[center_62%]"
            />
            <div className="absolute inset-0 z-[5] bg-black/55" />
            <div className="relative z-10 flex h-full flex-col">
                <div className="absolute inset-0 z-10 -mt-[1px] flex flex-col items-center justify-center gap-[14px]">
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
                    <Button variant="white_primary" className="mt-[5px] w-[249px]">
                        Посмотреть каталог
                    </Button>
                </div>
                <div className="absolute left-1/2 top-[87.7%] z-10 flex w-[1038px] -translate-x-1/2 items-center justify-center gap-[23px]">
                    <div className="flex items-center gap-4">
                        <CameraIcon />
                        <p className="text-[18px] text-white">
                            Фото вашего букета
                            <br />
                            перед отправкой
                        </p>
                    </div>
                    <div className="flex items-center gap-4">
                        <CarIcon />
                        <p className="text-[18px] text-white">
                            Наша доставка работает
                            <br />
                            24 часа в сутки
                        </p>
                    </div>
                    <div className="flex items-center gap-4">
                        <FlowerIcon />
                        <p className="text-[18px] text-white">
                            Соберите свой букет
                            <br />
                            в нашем конструкторе
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}
