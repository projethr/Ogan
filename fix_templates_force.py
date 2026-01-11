import os

base_html = r"""{% load static %}
<!DOCTYPE html>
<html lang="fr" class="light">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}OGAN by LSM{% endblock %}</title>
    <link href="{% static 'css/output.css' %}?v=1.1" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
        // Check local storage or system preference for dark mode
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
    </script>
</head>

<body class="bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans transition-colors duration-200">

    <!-- Navbar -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-50 transition-colors duration-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0 flex items-center">
                    <a href="{% url 'core:home' %}"
                        class="text-2xl font-bold text-gray-900 dark:text-white tracking-widest uppercase">
                        OGAN<span class="text-xs ml-1 font-light tracking-normal text-gray-500">by LSM</span>
                    </a>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden sm:ml-6 sm:flex sm:items-center sm:space-x-8">
                    <a href="{% url 'core:home' %}"
                        class="text-gray-900 dark:text-gray-300 hover:text-black dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Accueil</a>
                    <a href="{% url 'store:product_list' %}"
                        class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Catalogue</a>
                    <a href="{% url 'core:about' %}"
                        class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">À
                        propos</a>
                    <a href="{% url 'core:home' %}#footer"
                        class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">Contact</a>
                </div>

                <!-- Right Side: Dark Mode Toggle & Cart & Mobile Menu -->
                <div class="flex items-center space-x-4">
                    <button id="theme-toggle"
                        class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5">
                        <!-- Dark Icon -->
                        <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg">
                            <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                        </svg>
                        <!-- Light Icon -->
                        <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 100 2h1z"
                                fill-rule="evenodd" clip-rule="evenodd"></path>
                        </svg>
                    </button>

                    <a href="{% url 'orders:cart_detail' %}"
                        class="relative p-2 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                        </svg>
                        {% with cart_len=cart|length %}
                        {% if cart_len > 0 %}
                        <span
                            class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full">{{ cart_len }}</span>
                        {% endif %}
                        {% endwith %}
                    </a>

                    <!-- Mobile menu button -->
                    <button id="mobile-menu-button" type="button"
                        class="sm:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16m-7 6h7" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile menu, show/hide based on menu state. -->
        <div id="mobile-menu"
            class="hidden sm:hidden bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="{% url 'core:home' %}"
                    class="block text-gray-900 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 px-3 py-2 rounded-md text-base font-medium">Accueil</a>
                <a href="{% url 'store:product_list' %}"
                    class="block text-gray-900 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 px-3 py-2 rounded-md text-base font-medium">Catalogue</a>
                <a href="{% url 'core:home' %}#footer"
                    class="block text-gray-900 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 px-3 py-2 rounded-md text-base font-medium">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="min-h-screen">
        {% block content %}
        {% endblock %}
    </main>

    <footer id="footer"
        class="bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 py-16 transition-colors duration-200">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">

            <!-- Branding & Slogan -->
            <div class="space-y-4">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white tracking-[0.2em] uppercase">OGAN</h3>
                <p class="text-lg md:text-xl font-bold text-indigo-600 dark:text-indigo-400">
                    Commence, persévère et deviens OGAN 👑
                </p>
            </div>

            <!-- Contact Links -->
            <div class="flex flex-col items-center space-y-6">
                <div class="space-y-2">
                    <p class="text-sm font-semibold text-gray-950 dark:text-gray-100">
                        🧢 Voir le catalogue & commander :
                    </p>
                    <a href="https://wa.me/c/22943803804" target="_blank"
                        class="text-indigo-600 dark:text-indigo-400 hover:underline text-lg font-medium">
                        👉 https://wa.me/c/22943803804
                    </a>
                </div>

                <div class="space-y-2">
                    <p class="text-sm font-semibold text-gray-950 dark:text-gray-100">
                        📩 Boutique WhatsApp (commandes) :
                    </p>
                    <a href="https://wa.me/22943803804" target="_blank"
                        class="text-indigo-600 dark:text-indigo-400 hover:underline text-lg font-medium">
                        👉 wa.me/22943803804
                    </a>
                </div>

                <div class="space-y-2">
                    <p class="text-sm font-semibold text-gray-950 dark:text-gray-100">
                        📞 Contact direct – infos rapides (WhatsApp & appel) :
                    </p>
                    <p class="text-indigo-600 dark:text-indigo-400 text-lg font-bold tracking-wider">
                        👉 +229 01 51 48 07 42
                    </p>
                </div>
            </div>

            <!-- Bottom Copyright -->
            <div class="pt-8 border-t border-gray-100 dark:border-gray-700 w-full max-w-xs mx-auto">
                <p class="text-gray-400 dark:text-gray-500 text-[10px] uppercase tracking-widest font-medium">
                    &copy; 2026 OGAN by LSM. Tous droits réservés.
                </p>
            </div>
        </div>
    </footer>

    <script>
        var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
        var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

        // Change the icons inside the button based on previous settings
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            themeToggleLightIcon.classList.remove('hidden');
        } else {
            themeToggleDarkIcon.classList.remove('hidden');
        }

        var themeToggleBtn = document.getElementById('theme-toggle');

        themeToggleBtn.addEventListener('click', function () {
            // toggle icons inside button
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');

            // if set via local storage previously
            if (localStorage.theme) {
                if (localStorage.theme === 'light') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                }

                // if NOT set via local storage previously
            } else {
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                } else {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                }
            }
        });

        // Mobile menu toggle
        var mobileMenuBtn = document.getElementById('mobile-menu-button');
        var mobileMenu = document.getElementById('mobile-menu');

        mobileMenuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    </script>
</body>

</html>
"""

product_detail_html = r"""{% extends 'base.html' %}

{% block content %}
<div class="bg-white dark:bg-gray-800">
    <div class="max-w-2xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:max-w-7xl lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-x-8 lg:items-start">
            <!-- Image gallery -->
            <div class="flex flex-col-reverse">
                <div class="w-full aspect-w-1 aspect-h-1">
                    {% if product.image %}
                    <img src="{{ product.image.url }}" alt="{{ product.name }}"
                        class="w-full h-full object-center object-cover sm:rounded-lg">
                    {% else %}
                    <div class="w-full h-full flex items-center justify-center text-gray-500 bg-gray-100 sm:rounded-lg">
                        Pas d'image</div>
                    {% endif %}
                </div>
            </div>

            <!-- Product info -->
            <div class="mt-10 px-4 sm:px-0 sm:mt-16 lg:mt-0">
                <div class="flex flex-col space-y-4">
                    <nav class="flex" aria-label="Breadcrumb">
                        <ol role="list" class="flex items-center space-x-2">
                            <li>
                                <div class="flex items-center">
                                    <a href="{% url 'core:home' %}"
                                        class="text-xs font-medium text-gray-500 hover:text-gray-700 dark:text-gray-400">OGAN</a>
                                    <svg class="flex-shrink-0 h-4 w-4 text-gray-300 ml-2" fill="currentColor"
                                        viewBox="0 0 20 20">
                                        <path
                                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" />
                                    </svg>
                                </div>
                            </li>
                            <li>
                                <div class="flex items-center">
                                    <span
                                        class="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-widest">{{ product.category.name }}</span>
                                </div>
                            </li>
                        </ol>
                    </nav>

                    <h1 class="text-4xl font-black tracking-tight text-gray-900 dark:text-white uppercase">{{ product.name }}</h1>

                    <div class="flex items-center space-x-4">
                        <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ product.price }} <span
                                class="text-sm font-normal text-gray-500">CFA</span></p>
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {% if product.stock > 0 %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400{% else %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400{% endif %}">
                            {% if product.stock > 0 %}En stock{% else %}Épuisé{% endif %}
                        </span>
                    </div>

                    <div class="mt-6">
                        <h3 class="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-2">
                            Description</h3>
                        <div class="text-base text-gray-600 dark:text-gray-400 leading-relaxed max-w-prose">
                            {{ product.description|linebreaks }}
                        </div>
                    </div>

                    <div class="mt-8 border-t border-gray-100 dark:border-gray-700 pt-8">
                        <form method="post" action="{% url 'orders:cart_add' product.id %}" class="space-y-6">
                            {% csrf_token %}
                            <div class="flex items-center space-x-4">
                                <div
                                    class="flex items-center border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden h-12">
                                    <button type="button" onclick="this.nextElementSibling.stepDown()"
                                        class="px-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400">-</button>
                                    <input type="number" name="quantity" value="1" min="1" max="{{ product.stock }}"
                                        class="w-12 text-center border-none bg-transparent focus:ring-0 text-sm font-bold text-gray-900 dark:text-white"
                                        readonly>
                                    <button type="button" onclick="this.previousElementSibling.stepUp()"
                                        class="px-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400">+</button>
                                </div>
                                <button type="submit" {% if product.stock == 0 %}disabled{% endif %}
                                    class="flex-1 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 py-3 px-8 rounded-lg font-bold uppercase tracking-wider hover:bg-indigo-600 dark:hover:bg-indigo-400 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed h-12">
                                    Ajouter au panier
                                </button>
                            </div>
                        </form>
                    </div>

                    <div class="grid grid-cols-2 gap-4 mt-8">
                        <div
                            class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-100 dark:border-gray-700">
                            <svg class="h-6 w-6 text-indigo-600 mb-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M5 13l4 4L19 7" />
                            </svg>
                            <h4 class="text-xs font-bold uppercase text-gray-900 dark:text-white">Qualité Premium</h4>
                            <p class="text-[10px] text-gray-500">Matériaux sélectionnés avec soin.</p>
                        </div>
                        <div
                            class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-100 dark:border-gray-700">
                            <svg class="h-6 w-6 text-indigo-600 mb-2" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <h4 class="text-xs font-bold uppercase text-gray-900 dark:text-white">Livraison Express</h4>
                            <p class="text-[10px] text-gray-500">Livré chez vous rapidement.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

home_html = r"""{% extends 'base.html' %}
{% load static %}

{% block content %}
<!-- Hero Section -->
<div class="relative bg-white dark:bg-gray-800 overflow-hidden">
    <div class="max-w-7xl mx-auto">
        <div
            class="relative z-10 pb-8 bg-white dark:bg-gray-800 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <svg class="hidden lg:block absolute right-0 inset-y-0 h-full w-48 text-white dark:text-gray-800 transform translate-x-1/2"
                fill="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
                <polygon points="50,0 100,0 50,100 0,100" />
            </svg>

            <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                <div class="sm:text-center lg:text-left">
                    <h1
                        class="text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
                        <span class="block xl:inline">Jeunesse ambitieuse,</span>
                        <span class="block text-indigo-600 xl:inline">consciente & disciplinée.</span>
                    </h1>
                    <p
                        class="mt-3 text-base text-gray-500 dark:text-gray-300 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                        Découvrez OGAN, la marque de casquettes premium pour ceux qui osent rêver et agir. Rejoignez le
                        mouvement.
                    </p>
                    <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                        <div class="rounded-md shadow">
                            <a href="{% url 'store:product_list' %}"
                                class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10">
                                Voir le catalogue
                            </a>
                        </div>
                        <div class="mt-3 sm:mt-0 sm:ml-3">
                            <a href="{% url 'core:about' %}"
                                class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 dark:bg-gray-700 dark:text-indigo-400 hover:bg-indigo-200 dark:hover:bg-gray-600 md:py-4 md:text-lg md:px-10">
                                Notre vision
                            </a>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
        <img class="h-56 w-full object-cover sm:h-72 md:h-96 lg:w-full lg:h-full"
            src="{% static 'img/ogan_brand_image.png' %}" alt="OGAN Cap">
    </div>
</div>

<!-- Featured Section (Placeholder) -->
<section class="py-12 bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
            <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Collection</h2>
            <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
                Nos modèles phares
            </p>
            <p class="mt-4 max-w-2xl text-xl text-gray-500 dark:text-gray-300 lg:mx-auto">
                Design épuré, qualité premium.
            </p>
        </div>

        <div class="mt-12 grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
            {% for product in products %}
            <div
                class="group relative bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div
                    class="w-full min-h-80 bg-gray-200 aspect-w-1 aspect-h-1 rounded-t-lg overflow-hidden group-hover:opacity-75 lg:h-80 lg:aspect-none">
                    {% if product.image %}
                    <img src="{{ product.image.url }}" alt="{{ product.name }}"
                        class="w-full h-full object-center object-cover lg:w-full lg:h-full">
                    {% else %}
                    <div
                        class="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-700 text-gray-400">
                        <svg class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    </div>
                    {% endif %}
                </div>
                <div class="px-4 py-4">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                                <a href="{% url 'store:product_detail' product.slug %}">
                                    <span aria-hidden="true" class="absolute inset-0"></span>
                                    {{ product.name }}
                                </a>
                            </h3>
                            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 capitalize">{{ product.category.name }}</p>
                        </div>
                        <p class="text-lg font-bold text-indigo-600 dark:text-indigo-400">{{ product.price }} CFA</p>
                    </div>
                    <div class="mt-4">
                        <div class="flex items-center justify-between text-sm">
                            <span
                                class="px-2 py-1 rounded-full text-xs font-semibold {% if product.stock > 0 %}bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200{% else %}bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200{% endif %}">
                                {% if product.stock > 0 %}En Stock{% else %}Épuisé{% endif %}
                            </span>
                            <span class="text-indigo-600 dark:text-indigo-400 group-hover:underline">Voir détails
                                &rarr;</span>
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-span-full text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Aucun produit</h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Le catalogue est cours de mise à jour.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
"""

files = {
    r"templates/base.html": base_html,
    r"templates/store/product_detail.html": product_detail_html,
    r"templates/core/home.html": home_html,
}

for path, content in files.items():
    try:
        # Construct absolute path assuming run from root d:\Projet Ogan
        full_path = os.path.abspath(path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully wrote {path}")
    except Exception as e:
        print(f"Failed to write {path}: {e}")
