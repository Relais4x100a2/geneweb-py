**DO NOT CHANGE THIS FILE**

# .gw format 📜

The `.gw` source file format is used by GeneWeb to create a genealogy base (using the `gwc` command). GeneWeb is also capable of producing a `.gw` file, for archival or exchange.

The `.gw` file format is text based, machine as well as human readable, allowing for editing with any classical text editor and program manipulation. The `.gw` format is the best form for archival of a base (see caveats about isolated persons or pages) and for exchange with other GeneWeb users. GeneWeb is also capable of creating and producing GEDCOM format files, but the compatibility is not guaranteed (no information is lost as GeneWeb keep in textual notes any GEDCOM information it does not know how to handle).

With GeneWeb version 7.00, the `.gw` format has been augmented to allow for events (**gwplus**, see section [General structure of a .gw file](https://www.google.com/search?q=%23general-structure-of-a-gw-file) below). Additionnaly, version 7.01 will remove duplicate information between `fam` definitions and `fevents` or `pevents`. All details will be gathered into those events. Version 7.01 will maintain backward compatibility and read correctly `.gw` files created with older versions.

At this time, a `.gw` file does not remember the GeneWeb version it was created with. This may change.

**Warning**: older versions of GeneWeb (\< 7.00) cannot read the gwplus extensions of the `.gw` files. To alleviate this problem, the `gwu` command has been augmented to include an option (`-old_gw`) which transfers into the notes field any incompatible information.

## Style guide

  * Text that should appear "as is" will be **bold**.
  * Words in *italic* are replaced by their effective value. Their first letter is uppercase, e.g. *HusbandLastName*
  * Parameters between [brackets] are optionals.
  * Parameters separated by '|' are alternatives: only one choice is selected.

Definition example:

```
fam HusbandLastName FirstName[.Number] + [WeddingDate] [#mp WeddingPlace] WifeLastName FirstName[.Number]
```

Valid examples:

```
fam CORNO Joseph_Marie_Vincent + THOMAS Marie_Julienne
fam CORNO Alain.1 +25/11/1728 #mp Ile-aux-Moines CAUZIC Marie
```

-----

## Dates

Dates formats adhere to the european standard: dd/mm/yyyy, yyyy, mm/yyyy. An unknown but mandatory dates is "0".

Prefix modifiers can be used to specify "about", "before", "may-be" "after" etc.

| Type de date | Caractère spécial | Exemple |
| :--- | :--- | :--- |
| About | `~` | `~10/5/1990` |
| May be | `?` | `?10/5/1990` |
| Before | `<` | `<10/5/1990` |
| After | `>` | `>10/5/1990` |
| Or | `|` | `10/5/1990\|1991` |
| Between | `..` | `10/5/1990..1991`|

The calendar is Gregorian by default. For Julian, add a "J" at the end of the date, "F" for French Republic, and "H" Hebrew. Exemple : `10/9/5750H`

To enter a date in simple text form, prefix it with "0" between parenthesis:

```
0(5_Mai_1990)
```

-----

## Character strings

Spaces within strings are replaced by underscore `_` (except in notes and in some comments) : `Marie_Julienne`

ASCII uppercase follow ISO-8859-1.

-----

## Referencing a person

The same person may be referenced several times in a `.gw` file; as a parent, as a child or as a relation (witness, god parent, ...). LastName, FirstName and occurence number (if necessary) must match exactly for GeneWeb to establish the correspondence.

-----

## General structure of a .gw file

```
[encoding: utf-8]	# (optional) redefines text encoding to be utf-8 instead of iso-8859-1
[gwplus]			# (optional) specifies that this file follows the gwplus instead of gw format
```

any number of the following :

```
Family         	# start token is fam
PersonalNote 	# start token is notes
Relations      	# start token is rel
PersonEvents  	# start token is pevt (specific to gwplus)
DataBaseNotes 	# start token is notes-db (only one)
ExtendedPages 	# start token is page-ext
WizardNotes  	# start token is wizard-note (potentially one for each wizard)
```

See in the sections below the end token for each block.

-----

## Main structure : family

The principal information structuring a GeneWeb base is the "family". A family is comprised of a Husband, a Wife and Children (note that the sex verification of husband and wife can be turned off). Personal information (DoB, etc.) is attached to children. If a spouse does not have parents, its personal informations are inserted after its name in the family definition.

**Case \# 1 : Both spouses are already mentioned as child of a family.**

```
 fam HusbandLastName FirstName[.Number] [PersonDetails] +[WeddingDate]
  [#nm | #eng]  [ [#nsck | #nsckm | #noment | #banns | #contract | #license | #pacs | #residence] [m | f | ?][m | f | ?] ]
  [#mp WeddingPlace] [#ms WeddingSource]
  [#sep | - DivorceDate]
  WifeLastName FirstName[.Number]   # family arguments should be on a single line
  [wit[ m| f|]: Witness (use Person format, see Person Information section) ]  # possibly several witnesses, respect spaces
  [src Family source]
  [comm Family comments in free format]
  [cbp common children birth place]
  [csrc common children source]
 [fevt 
    FamilyEvent (multiples)
 end fevt]
 [beg
 - [h | f |  ] Person # see detailed description at the next section
 end]
```

  * If the spouses are not married (relation), insert the tag **\#nm**. If they are engaged, use **\#eng**.
  * If the spouses are separated, use **\#sep**. If they are divorced, use **-** and provide the (optional) divorce date.
  * If *ChildLastName* is absent, that of the father will be used.
  * All the information associated with the **fam** tag must appear on a single line.
  * Tags **wit**, **src** and **comm** follow on separate lines, after **fam**. They are optionals.
  * If the child sex is unknown, no **h** nor **f** after the **-** (dash).

If the family has no child, the tags **beg**/**end** can be omitted :

```
fam HEYDENREICH Gaspard +1719 TRESCH Rosine_Catherine
```

**Case \#2: One or both spouses are not already listed as child of a family.** In this case, their LastName FirstName information is followed by their personal information as done for a child. See section [\#Personal information](https://www.google.com/search?q=%23personal-information) below for more details.

Example : John Corno (o 1935 at Soisy, +1997) Direct entry of personal information:

```
fam Corno John 1935 #bp Soisy 1997 + Rempp Zabeth
```

If there is no personal information associated with a person, then enter the number 0 following his LastName/FirstName which will be used as default DoB and mark that this person is not defined anywhere else. If the spouse is unknown, provide two question mark separated by a space (**? ?**):

```
fam Diemer Patrick 0 + Heidenreich Sylvie 0
fam Doe John 0 + ? ?
```

### FamilyEvent structure

This sub-section is specific to **gwplus** format.

```
FamilyEventName [EventDate] [#p EventPlace] [#s EventSource]
[wit[ m| f]: Person ]	
[note One line of free text] # multiple note lines until FamilyEventName or end_fevt

FamilyEventNames
#marr  -> (Efam_Marriage)
#nmar  -> (Efam_NoMarriage)
#nmen  -> (Efam_NoMention)
#enga  -> (Efam_Engage)
#div   -> (Efam_Divorce)
#sep   -> (Efam_Separated)
#anul  -> (Efam_Annulation)
#marb  -> (Efam_MarriageBann)
#marc  -> (Efam_MarriageContract)
#marl  -> (Efam_MarriageLicense)
#pacs  -> (Efam_PACS)
#resi  -> (Efam_Residence)
#strng -> (Efam_Name strng)
```

Note that certain events may be described both within personal information in a **fam** record (`#mp` = marriage place) and in an **fevt** sub-record (`#p` = place of event). The same information will appear at both places for events such as marriage. In the case of hand edited source files, the information appearing in the **fevt** sub-record takes precedence over the information kept in the **fam** line (this means that if no information appears in the **fevt** sub-record, the information on the **fam** line will be lost).

Note that the **+** token in the **fam** line indicates the beginning of a relation description, and does not necessarily imply a marriage : the tag **\#nm** in the **fam** line, or **\#nmar** in the **fevt** sub-record indicates a relation without marriage. If **\#nm** and **\#nmar** are absent, then a marriage is assumed.

The tag **\#noment** in the **fam** line or **\#nmen** in the **fevt** sub-record creates a relation event with no name.

-----

## Personal information

Personal information may appear next to a child on a **fam** record, or next to the spouse description of the person is not described as a child elsewhere. Personal information may also appear in relation structures (**rel**, see section below) if it is impossible to put it in a family structure (for example, for an adopted child).

The strict minimum for personal information is LastName, FirstName, optional occurence number and `0` as DoB.:

```
Corno Yann 0
```

For a child, DoB is not mandatory.

In summary DoB (Date of Birth) is only mandatory if the person is a parent, or has a DoD. In this last case, if the DoB is unknown, use 0.

Example : Maurice, DoB unknown, died in 1935 in Caen :

```
Corno Maurice 0 1935 #dp Caen
```

The full format definition for a person follows:

```
 LastName FirstName[.Number] 
   [(PublicName)] [#nick Qualifier]
   [{FirstNameAlias}] [#salias SurnameAlias]  [#alias Alias] 
   [[Title (see Title section)]] [#apubl | #apriv]
   [#image ImageFilePath]  
   [#occu Occupation] [#src PersonSource] 
 DateOfBirth  [#bp PlaceOfBirth] [#bs BirthSource]
   [!BaptizeDate] [#pp BaptizePlace] [#ps BaptizeSource] 
 [#od] [DateOfDeath] [#dp PlaceOfDeath] [#ds DeathSource] 
   [#buri | #crem [BurialDate]] [#rp BurialPlace] [#rs BurialSource]
```

  * See comments above about DoB obligations.
  * If one does not know wether a person is still alive, use **?** for DoD (Date of Death).
  * If the person is "obviously" dead (born more than 150 ago for instance) use the **\#od** tag (evolution after GeneWeb 5.?).
  * If the person died in its early years, use the **\#mj** tag.
  * **\#apubl** and **\#apriv** provide access control: Public (anybody) or Private (wizards or friends). If nothing is provided, the "If Titles" rule applies.

The kind of death may be specified with a prefix modifier:

| Type of death | Special character | Example |
| :--- | :--- | :--- |
| Killed | `k` | `k10/5/1990` |
| Murdered | `m` | `m10/5/1990` |
| Executed | `e` | `e10/5/1990` |
| Disappeared | `s` | `s10/5/1990` |

Use the **\#buri** or **\#crem** tags to specify burial or cremation details.

### Titles

While titles are part of the personal information section, they are described here in more details for better understanding. Titles are describer between brackets **[ ]** (Ooops, those brackets are full part of the format ...). If there are multiple titles, they are appended one after the other with a new bracket pair.

```
[ TitleName:Title:TitlePlace:StartDate:EndDate:Nth]
```

  * Each item is separated by a '**:'.** If no information is available, leave an empty item.
  * The main title is designated as '**\***' as TitleName.

### Personal events

This sub-section is specific to **gwplus** format.

```
pevt PersonLastName PersonFirstName[.Number]
OnePersonEvent (multiples)
end pevt
```

Each *OnePersonEvent* has the following structure:

```
PersonEventName [EventDate] [#p EventPlace] [#s EventSource]
 [wit[ m| f]: [#godp | #offi | ] Person  ] #multiple witness (#offi not yet implemented)
 [note One line of free text] # multiple lines

PersonEventNames 
 #birt  -> (Epers_Birth)
 #bapt  -> (Epers_Baptism)
 #deat  -> (Epers_Death)
 #buri  -> (Epers_Burial)
 #crem  -> (Epers_Cremation)
 #acco  -> (Epers_Accomplishment)
 #acqu  -> (Epers_Acquisition)
 #adhe  -> (Epers_Adhesion)
 #bapl  -> (Epers_BaptismLDS)
 #barm  -> (Epers_BarMitzvah)
 #basm  -> (Epers_BatMitzvah)
 #bles  -> (Epers_Benediction)
 #cens  -> (Epers_Recensement)
 #chgn  -> (Epers_ChangeName)
 #circ  -> (Epers_Circumcision)
 #conf  -> (Epers_Confirmation)
 #conl  -> (Epers_ConfirmationLDS)
 #degr  -> (Epers_Diploma)
 #awar  -> (Epers_Decoration)
 #demm  -> (Epers_DemobilisationMilitaire)
 #dist  -> (Epers_Distinction)
 #endl  -> (Epers_Dotation)
 #dotl  -> (Epers_DotationLDS)
 #educ  -> (Epers_Education)
 #elec  -> (Epers_Election)
 #emig  -> (Epers_Emigration)
 #exco  -> (Epers_Excommunication)
 #flkl  -> (Epers_FamilyLinkLDS)
 #fcom  -> (Epers_FirstCommunion)
 #fune  -> (Epers_Funeral)
 #grad  -> (Epers_Graduate)
 #hosp  -> (Epers_Hospitalisation)
 #illn  -> (Epers_Illness)
 #immi  -> (Epers_Immigration)
 #lpas  -> (Epers_ListePassenger)
 #mdis  -> (Epers_MilitaryDistinction)
 #mpro  -> (Epers_MilitaryPromotion)
 #mser  -> (Epers_MilitaryService)
 #mobm  -> (Epers_MobilisationMilitaire)
 #natu  -> (Epers_Naturalisation)
 #occu  -> (Epers_Occupation)
 #ordn  -> (Epers_Ordination)
 #prop  -> (Epers_Property)
 #cens  -> (Epers_Recensement)
 #resi  -> (Epers_Residence)
 #reti  -> (Epers_Retired)
 #slgc  -> (Epers_ScellentChildLDS)
 #slgp  -> (Epers_ScellentParentLDS)
 #slgs  -> (Epers_ScellentSpouseLDS)
 #vteb  -> (Epers_VenteBien)
 #will  -> (Epers_Will)
 #strng -> (Epers_Name strng)
```

-----

## Notes

Notes are associated to one person and stored as free form text between **notes** and **end notes** tags:

```
 notes LastName FirstName[.Number]
 beg
 Notes go here in a totally free format 
 (HTML tags can be inserted here. See the -tags option for gwd and tags.txt file))
 end notes
```

-----

## Relations

Relations associated with one person and are stored separately, as for notes. In the following list, all possible markers are mentioned when only one is typically used.

```
rel LastName FirstName[.Number]
beg
- adop: AdoptiveFather + AdoptiveMother
- adop fath: AdoptiveFather
- adop moth: AdoptiveMother
- reco: RecognizingFather + RecognizingMother
- reco fath: RecognizingFather
- reco moth: RecognizingMother
- cand: CandidateFather + CandidateMother
- cand fath: CandidateFather
- cand moth: CandidateMother
- godp: GodFather + GodMother
- godp fath: GodFather
- godp moth: GodMother
- fost: FosterFather + FosterMother
- fost fath: FosterFather
- fost moth: FosterMother
end
```

-----

## DataBaseNote

The DataBase Note is the text that appears when one clicks on the "Note de présentation" tag of the Welcome page.

```
notes-db
  Free text starting with two spaces (including HTML and WiKi syntax formatting)
end notes-db
```

-----

## ExtendedPages

Extended pages are pages referenced within persons notes using the WiKi syntax `[[[ExtendedPageName/Free text]]]`. The same syntax can be used within extended pages themselves.

```
# extended page "PageName" used by:
#  - person "PersonFirstName[.Number] PersonLastName" 	# multiple lines indicating usage by Person (two spaces before -)
#  - extended page "PageName"                  	        # or by other ExtendedPage
page-ext PageName
  Free text with two spaces at the beginning of each line.
  Free text may contain HTML and WiKi formatting commands.
  Continued free text 
end page-ext
```

-----

## WizardPage

```
Wizard-note Wizard_name
  timestamp                        # page creation date timestamp computed as the number of seconds since january 1st,1970 (unix epoch)
  Free text following WiKiText format describing the wizard and his activities.
  Each line begins with two spaces.
end wizard-note
```

Each wizard may have a page describing his activities and his background. If the parameter `authorized_wizards_notes` is positionned to `yes` in the `basename.gwf` file, the welcome page will propose a link to a page showing all active wizard notes sorted in alphabetical order.

Each wizard can edit the content of his own page.