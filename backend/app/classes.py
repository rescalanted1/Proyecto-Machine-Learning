"""
PlantVillage class definitions — 15 classes.

The index order MUST match the order used during model training.
Standard PlantVillage alphabetical order is assumed.
"""

CLASS_INFO: dict[int, dict] = {
    0: {
        "name": "Pepper bell Bacterial spot",
        "name_es": "Pimiento — Mancha Bacteriana",
        "plant": "Pimiento (Capsicum annuum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "La mancha bacteriana del pimiento es causada por Xanthomonas campestris. "
            "Produce lesiones acuosas de color marrón oscuro en hojas y frutos. "
            "Las hojas severamente infectadas se vuelven amarillas y caen prematuramente, "
            "reduciendo la fotosíntesis y el rendimiento del cultivo."
        ),
        "treatment": (
            "Aplicar bactericidas o compuestos a base de cobre preventivos. "
            "Retirar y destruir de inmediato las hojas y frutos infectados para evitar la propagación. "
            "Evitar el riego por aspersión para no dispersar las bacterias por salpicaduras."
        ),
    },
    1: {
        "name": "Pepper bell healthy",
        "name_es": "Pimiento — Saludable",
        "plant": "Pimiento (Capsicum annuum)",
        "is_healthy": True,
        "severity": "none",
        "description": (
            "La planta de pimiento se encuentra en estado saludable. "
            "No se detectan signos de enfermedades, plagas o deficiencias nutricionales. "
            "Continúe con las prácticas de manejo habituales para mantener la salud del cultivo."
        ),
        "treatment": (
            "Mantener el régimen de riego óptimo y la fertilización programada. "
            "Realizar inspecciones preventivas semanales para asegurar la detección oportuna de anomalías."
        ),
    },
    2: {
        "name": "Potato Early blight",
        "name_es": "Papa — Tizón Temprano",
        "plant": "Papa (Solanum tuberosum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "El tizón temprano de la papa es causado por el hongo Alternaria solani. "
            "Se caracteriza por manchas marrones con anillos concéntricos ('ojo de buey') "
            "en las hojas más viejas. Puede causar defoliación severa y reducir "
            "significativamente el rendimiento de los tubérculos."
        ),
        "treatment": (
            "Aplicar fungicidas protectores como clorotalonil o mancozeb. "
            "Eliminar los restos de hojas infectadas tras la cosecha y asegurar una buena fertilización "
            "con nitrógeno para fortalecer la resistencia de la planta."
        ),
    },
    3: {
        "name": "Potato Late blight",
        "name_es": "Papa — Tizón Tardío",
        "plant": "Papa (Solanum tuberosum)",
        "is_healthy": False,
        "severity": "critical",
        "description": (
            "El tizón tardío es causado por el oomicete Phytophthora infestans. "
            "Es una de las enfermedades más devastadoras de la papa. Produce lesiones "
            "acuosas de color verde oscuro a negro en hojas y tallos, con un moho "
            "blanquecino en el envés de la hoja. Puede destruir un cultivo completo "
            "en pocos días bajo condiciones favorables."
        ),
        "treatment": (
            "Aplicar fungicidas sistémicos específicos inmediatamente. "
            "Destruir por completo el follaje infectado. Evitar el exceso de humedad en el suelo "
            "y no regar durante las horas de la tarde para evitar que las hojas queden húmedas por la noche."
        ),
    },
    4: {
        "name": "Potato healthy",
        "name_es": "Papa — Saludable",
        "plant": "Papa (Solanum tuberosum)",
        "is_healthy": True,
        "severity": "none",
        "description": (
            "La planta de papa se encuentra en estado saludable. "
            "No se detectan signos de tizón temprano, tizón tardío u otras "
            "enfermedades. Mantenga las prácticas de riego y fertilización adecuadas."
        ),
        "treatment": (
            "Continuar con riegos regulares sin encharcamientos. "
            "Asegurar una ventilación adecuada entre surcos para minimizar el riesgo de humedad foliar acumulada."
        ),
    },
    5: {
        "name": "Tomato Bacterial spot",
        "name_es": "Tomate — Mancha Bacteriana",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "La mancha bacteriana del tomate es causada por varias especies de "
            "Xanthomonas. Produce pequeñas lesiones oscuras, acuosas y angulares "
            "en hojas, tallos y frutos. Las hojas afectadas se tornan amarillas "
            "y pueden caer, exponiendo los frutos a quemaduras solares."
        ),
        "treatment": (
            "Aplicar compuestos a base de cobre en combinación con mancozeb para mejorar la eficacia. "
            "Desinfectar rigurosamente las herramientas de poda y evitar el trabajo en el cultivo "
            "cuando las plantas estén húmedas."
        ),
    },
    6: {
        "name": "Tomato Early blight",
        "name_es": "Tomate — Tizón Temprano",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "El tizón temprano del tomate es causado por Alternaria solani. "
            "Se manifiesta con manchas marrones concéntricas en las hojas inferiores. "
            "Si no se controla, puede causar defoliación severa, reduciendo "
            "drásticamente el rendimiento y exponiendo los frutos a quemaduras solares."
        ),
        "treatment": (
            "Podar las hojas inferiores afectadas para cortar la fuente de inóculo y mejorar la aireación. "
            "Aplicar fungicidas preventivos como clorotalonil o fungicidas biológicos a base de Bacillus subtilis."
        ),
    },
    7: {
        "name": "Tomato Late blight",
        "name_es": "Tomate — Tizón Tardío",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "critical",
        "description": (
            "El tizón tardío del tomate es causado por Phytophthora infestans. "
            "Produce grandes manchas acuosas de color verde grisáceo a marrón "
            "en las hojas y tallos, con un moho blanquecino visible en condiciones "
            "húmedas. Es altamente destructivo y se propaga rápidamente."
        ),
        "treatment": (
            "Eliminar y quemar de inmediato las plantas severamente infectadas. "
            "Aplicar fungicidas curativos y preventivos de amplio espectro. Reducir drásticamente "
            "la humedad ambiental y suspender el riego aéreo."
        ),
    },
    8: {
        "name": "Tomato Leaf Mold",
        "name_es": "Tomate — Moho Foliar",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "moderate",
        "description": (
            "El moho foliar del tomate es causado por el hongo Passalora fulva "
            "(antes Cladosporium fulvum). Produce manchas amarillentas en el haz "
            "de las hojas y un moho aterciopelado verde oliva a marrón en el envés. "
            "Es más común en invernaderos con alta humedad."
        ),
        "treatment": (
            "Aumentar significativamente la ventilación del invernadero para mantener la humedad por debajo del 85%. "
            "Aplicar fungicidas a base de cobre o azufre si aparecen los primeros síntomas en el envés."
        ),
    },
    9: {
        "name": "Tomato Septoria leaf spot",
        "name_es": "Tomate — Mancha Foliar por Septoria",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "La mancha foliar por Septoria es causada por el hongo Septoria lycopersici. "
            "Produce numerosas manchas pequeñas, circulares, con centro gris claro "
            "y borde oscuro. Comienza en las hojas inferiores y progresa hacia arriba, "
            "causando defoliación severa."
        ),
        "treatment": (
            "Retirar las hojas inferiores infectadas de la base de la planta. "
            "Regar a nivel del suelo para evitar humedecer el follaje. Aplicar fungicidas "
            "adecuados para hongos foliares."
        ),
    },
    10: {
        "name": "Tomato Spider mites (Two-spotted spider mite)",
        "name_es": "Tomate — Ácaro Araña de Dos Puntos",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "moderate",
        "description": (
            "El ácaro araña de dos puntos (Tetranychus urticae) es una plaga "
            "que succiona la savia de las hojas, causando un punteado amarillo "
            "o bronceado. En infestaciones severas, las hojas se secan y caen. "
            "Se reconoce por la presencia de telarañas finas en el envés de las hojas."
        ),
        "treatment": (
            "Aplicar jabón potásico o aceite de neem para sofocar a los ácaros. "
            "Aumentar la humedad ambiental pulverizando agua limpia, ya que los ácaros "
            "se reproducen con mayor rapidez en climas cálidos y secos."
        ),
    },
    11: {
        "name": "Tomato Target Spot",
        "name_es": "Tomate — Mancha en Diana",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "moderate",
        "description": (
            "La mancha en diana del tomate es causada por el hongo Corynespora cassiicola. "
            "Produce lesiones circulares con anillos concéntricos que recuerdan una diana. "
            "Afecta hojas, tallos y frutos, pudiendo causar defoliación en climas "
            "cálidos y húmedos."
        ),
        "treatment": (
            "Mejorar la circulación del aire mediante podas selectivas y espaciamiento de plantas. "
            "Aplicar fungicidas protectores a base de cobre o fungicidas sistémicos autorizados."
        ),
    },
    12: {
        "name": "Tomato Yellow Leaf Curl Virus",
        "name_es": "Tomate — Virus del Rizado Amarillo",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "critical",
        "description": (
            "El TYLCV (Tomato Yellow Leaf Curl Virus) es transmitido por la mosca "
            "blanca (Bemisia tabaci). Causa un amarillamiento y enrollamiento severo "
            "de las hojas, enanismo de la planta y reducción drástica de la producción. "
            "No tiene cura; el manejo se centra en el control del vector."
        ),
        "treatment": (
            "Colocar trampas cromáticas amarillas para capturar moscas blancas adultas. "
            "Usar mallas anti-insectos en invernaderos y aplicar insecticidas específicos o "
            "aceites minerales para reducir la población del vector."
        ),
    },
    13: {
        "name": "Tomato mosaic virus",
        "name_es": "Tomate — Virus del Mosaico",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": False,
        "severity": "high",
        "description": (
            "El virus del mosaico del tomate (ToMV) causa un patrón de mosaico "
            "de áreas claras y oscuras en las hojas, distorsión foliar y enanismo. "
            "Se transmite mecánicamente y por semillas contaminadas. No tiene cura; "
            "se previene con semillas certificadas y desinfección de herramientas."
        ),
        "treatment": (
            "Eliminar y destruir de inmediato las plantas que muestren síntomas de mosaico. "
            "Desinfectar las manos y las herramientas de trabajo utilizando una solución de leche descremada "
            "o fosfato trisódico antes de tocar plantas sanas."
        ),
    },
    14: {
        "name": "Tomato healthy",
        "name_es": "Tomate — Saludable",
        "plant": "Tomate (Solanum lycopersicum)",
        "is_healthy": True,
        "severity": "none",
        "description": (
            "La planta de tomate se encuentra en estado saludable. "
            "No se detectan signos de enfermedades fúngicas, bacterianas, virales "
            "ni daños por plagas. Continúe con las prácticas de manejo habituales."
        ),
        "treatment": (
            "Mantener prácticas de riego regulado por goteo para evitar mojar el follaje. "
            "Monitorear periódicamente el envés de las hojas inferiores para detectar plagas tempranas."
        ),
    },
}

# Total number of classes the model outputs
NUM_CLASSES = len(CLASS_INFO)
