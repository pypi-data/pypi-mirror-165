<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"		
  exclude-result-prefixes="formx config of svg dr3d calcext loext form field script chart">
    
<xsl:output method="xml" encoding="UTF-8" indent="no"/>
    
<!-- ### CLEANUP.XSL objectifs et description

À l'issue de cette transformation :

* Niveaux de titres
- le titre principal du document est ramené à un élément text:h[@text:outline-level='0'] (sources MS Word ou Libre Office) ;
- les niveaux de titres pour constuire l'arborescence sont ensuite uniformément balisés : <text:h> avec un attribut @text:outline-level associé ;
* Attributs
- tous les attributs sont conservés (<xsl:copy-of select="@*"/>) ;
* Enrichissements typographiques
- les raccourcis vers les enrichissements typographiques et leurs propriétés sont ramenés à la liste des propriétés, séparés par un espace (token) ;
- liste des propriétés conservées : italique, gras, exposant, indice, souligné, barré, petites-capitales (+ combinaison) ;
* Nettoyage
- suppression des éléments hérités du logiciel, des caractères de saut, par défaut… (voir liste infra) ;
- suppression de l'exposant autour des éléments de notes ;

Prérequis dans la construction du modèle de stylage : 
- pas d'héritage dans la création du style ;

XSL auxiliaire : 
- extract_style-name.xsl (extraction des @text:style-name)

Q & Remarques : 
- gestion des namespaces ;
- double-barré double-souligné à traiter (?)

Todo (ec)
- ajouter une préparation des tableaux, des listes (<text:list @xml:id text:style-name="WW8Num3">) ?
- suppression des sections 
    - voir fichier Franco Bruni
    - voir modalités de traitements des annexes et bibliographies
- style Footnote (style natif de Word) basé sur Standard…
- supprimer les paragraphes vides ?
- gestion des erreurs : cas de deux titres principaux OU pass 2 : si pas de outline-level=0 que faire ?
- /!\ Titre-section-biblio et Titre-section-annexe

* Suite ?
- table d'équivalence des noms de styles pour les ramener à un intitulé unique
-->
    
<!-- INCLUSION XSLT -->
<xsl:include href="list.xsl"/>
<xsl:include href="styles.xsl"/>
<xsl:include href="figures.xsl"/>
<xsl:include href="preserve.xsl"/>
<xsl:include href="delete.xsl"/>
        
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>
    
<!-- élément engloblant office:text (à conserver pour génération de la mainDiv) -->
<!-- A priori office:body est toujours présents dans les fichiers. office:text n'est plus à conserver pour génération de la mainDiv-->
<xsl:template match="office:text">
  <xsl:apply-templates/>
</xsl:template>

</xsl:stylesheet>