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
                <div className="absolute left-1/2 top-[87.7%] z-10 flex w-[1038px] -translate-x-1/2 items-center justify-center gap-[42px]">
                    <div className="flex h-16 w-[380px] flex-none grow-0 items-center gap-[20px] rounded-2xl border border-white/15 bg-black/25 px-3 py-2 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)] backdrop-blur-xxl backdrop-saturate-150">
                        <CameraIcon />
                        <p className="font-medium text-[20px] leading-[100%] text-white">
                            Фото вашего букета
                            <br />
                            перед отправкой
                        </p>
                    </div>
                    <div className="flex h-16 w-[380px] flex-none grow-0 items-center gap-[20px] rounded-2xl border border-white/15 bg-black/25 px-3 py-2 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)] backdrop-blur-xxl backdrop-saturate-150">
                        <CarIcon />
                        <p className="font-medium text-[20px] leading-[100%] text-white">
                            Наша доставка работает
                            <br />
                            24 часа в сутки
                        </p>
                    </div>
                    <div className="flex h-16 w-[380px] flex-none grow-0 items-center gap-[20px] rounded-2xl border border-white/15 bg-black/25 px-3 py-2 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)] backdrop-blur-xxl backdrop-saturate-150">
                        <FlowerIcon />
                        <p className="font-medium text-[20px] leading-[100%] text-white">
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
