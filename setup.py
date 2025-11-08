import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

requirements = ['paho-mqtt>=2.1.0']

setuptools.setup(
    # Имя дистрибутива пакета.
    name='pm_python_sdk',
    # Номер версии пакета.
    version='0.6.7',
    # Имя автора.
    author='Promobot',
    # Его почта.
    author_email='info@promo-bot.ru',
    # Краткое описание.
    description='SDK for Promobot manipulator control',
    # Длинное описание.
    long_description=long_description,
    # Определяет тип контента, используемый в long_description.
    long_description_content_type='text/markdown',
    # URL-адрес, представляющий домашнюю страницу проекта.
    url='https://promo-bot.ru/promobot-m-edu/',
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=setuptools.find_packages(),
    # requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
    # install_requires=requirements,
    # Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # Требуемая версия Python.
    python_requires='>=3.12',
)
