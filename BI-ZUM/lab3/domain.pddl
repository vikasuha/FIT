(define (domain sailor)

    (:requirements :strips)

    (:predicates
        (place ?place)
        (sailor ?sailor)
        (at ?where ?who)
        (path ?from ?to)
        (seapath ?from ?to)
        (atplacecan ?where ?act)
        (hasship)
        (hasfrigate)
        (hascaravels)
        (hasalkohol)
        (hasdoubtfulmeet)
        (hasflower)
        (hasbearleather)
        (hasmap)
        (hasgoldgroats)
        (hasgoldcoin)
        (hasgoldbrick)
        (hascriminalrecord)
        (hasalkomood)
        (hasintoxication)
        (hasdependence)
        (hasgoodconnect)
        (hasexperienceinfight)
        (hastree)
        (haspearl)
        (haswinpirates)
        (haswinbear)
        (hascoconuts)
        (hascocaine)
        (iscapitan)
        (hasdazzlegirl)
        (hasmeetsmuggler)
        (hashappiness)
        
    
    )


     (:action move
        :parameters (?who ?from ?to)
        :precondition (and (at ?from ?who) (path ?from ?to))
        :effect (and (at ?to ?who) (not (at ?from ?who)))
    )
    
    (:action sail
        :parameters (?who ?from ?to)
        :precondition (and (at ?from ?who)(seapath ?from ?to)(hasship))
        :effect (and (at ?to ?who) (not (at ?from ?who)))
    )
    
    (:action drunk1
        :precondition(and(hasalkohol)(not(hasintoxication))(not(hasalkomood)))
        :effect (and(hasalkomood)(not(hasalkohol)))
    )
    
    (:action drunk2
        :precondition(and(hasalkohol)(not(hasintoxication))(hasalkomood))
        :effect (and(hasintoxication)(not(hasalkohol)))
    )
    
    (:action drunk3
        :precondition(and(hasalkohol)(hasintoxication)(hasalkomood))
        :effect (and(hasdependence)(not(hasalkohol)))
    )
    
    (:action ship
        :precondition(and(hastree))
        :effect (and(hasship)(not(hastree)))
    )
    
    (:action frigate
        :precondition(and(hastree)(hasship)(hasgoldgroats))
        :effect (and(hasfrigate)(not(hasgoldgroats))(not(hastree)))
    )
    
    (:action frigate
        :precondition(and(hastree)(hasship)(hasgoldcoin))
        :effect (and(hascaravels)(not(hasgoldcoin))(not(hastree)))
    )
    
    
    (:action cutwood
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where cutwood))
        :effect (hastree)
    )
    
    (:action makeship
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where makeship)(hastree))
        :effect (hasship)
    )
    
    (:action pickflowers
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where pickflowers))
        :effect (hasflower)
    )
    
    (:action fightbear
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where fightbear))
        :effect (and(hasbearleather)(hasexperienceinfight)(haswinbear))
    )
    
    (:action meetmap
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where meetmap)(hasalkohol))
        :effect (and(hasmap)(not(hasalkohol))(hasdoubtfulmeet))
    )
    
    (:action stealship
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where stealship))
        :effect (and(hasship)(hascriminalrecord))
    )
    
    (:action pangold
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where pangold))
        :effect (and(hasgoldgroats))
    )
    
    (:action sober
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where sober))
        :effect (and(not(hasintoxication))(not(hasalkomood)))
    )
    
    (:action buyalko
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where buyalko)(hasgoldgroats))
        :effect (and(hasalkohol)(not(hasgoldgroats)))
    )
    
    (:action buyconnect
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where buyconnect)(hasgoldgroats))
        :effect (and(hasgoodconnect)(not(hasgoldgroats)))
    )
    
    (:action hardeninbattle
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where hardeninbattle)(hasalkomood))
        :effect (and(hasexperienceinfight))
    )
    
    (:action accumulate
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where accumulate)(hasgoldgroats))
        :effect (and(hasgoodconnect)(not(hasgoldgroats))(hasgoldcoin))
    )
    
    (:action invest
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where invest)(hasgoldcoin))
        :effect (and(hasgoodconnect)(not(hasgoldcoin))(hasgoldbrick))
    )
    
    (:action salecoconuts
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where salecoconuts)(hascoconuts))
        :effect (and(hasgoldcoin)(not(hascoconuts)))
    )
    
    (:action salebear
    :parameters (?where ?who)
    :precondition (and(at ?where ?who)(atplacecan ?where salecoconuts)(hasbearleather))
    :effect (and(hasgoldcoin)(not(hasbearleather)))
    )
    
    (:action work
    :parameters (?where ?who)
    :precondition (and(at ?where ?who)(atplacecan ?where work))
    :effect (and(hasgoldgroats))
    )
    
`   (:action meetsmuggler
    :parameters (?where ?who)
    :precondition (and(at ?where ?who)(atplacecan ?where meetsmuggler)(hasdoubtfulmeet)(hasgoldbrick))
    :effect (and(hasmeetsmuggler))
    )
    
    (:action stealmoney
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where stealmoney))
        :effect (and(hasgoldcoin)(hascriminalrecord))
    )
    
    
    (:action buyindulgence
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where buyindulgence)(hasgoldgroats))
        :effect (and(not(hasgoldgroats))(not(hascriminalrecord)))
    )
    
    (:action drunkcity
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where drunkcity))
        :effect (and(hasalkomood))
    )
    
    (:action study
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where study)(hasgoldcoin)(not(hascriminalrecord)))
        :effect (and(not(hasgoldcoin))(iscapitan))
    )
    
    (:action losingpirates
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where losingpirates)(not(hasexperienceinfight)))
        :effect (and(not(hasgoldcoin))(not(hasgoldgroats))(not(hasgoldbrick))(not(hascaravels))(not(hasfrigate)))
    )
    
    (:action joinpirates
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where joinpirates)(hasexperienceinfight))
        :effect (and(hasalkomood))
    )
    
    (:action winpirates
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where winpirates)(hasexperienceinfight)(hascaravels))
        :effect (and(hasgoldgroats)(hasgoldbrick)(hasgoldcoin)(hasship)(hasfrigate)(hascaravels)(haswinpirates))
    )
    
    (:action sinkforpearl
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where sinkforpearl))
        :effect (and(haspearl))
    )
    
    (:action dazzlegirl
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where dazzlegirl)(or(haswinpirates)(haswinbear)(iscapitan)))
        :effect (and(hasdazzlegirl))
    )
    
    (:action collectcoconuts
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where collectcoconuts))
        :effect (and(hascoconuts))
    )
    
    (:action findcocaine
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(atplacecan ?where findcocaine)(hasmap))
        :effect (and(hascocaine))
    )

    
    (:action goal_marry
        :parameters (?where ?who)
        :precondition (and (at ?where ?who)(hasdazzlegirl)(hasgoldbrick)(haspearl)(hasflower)(hasgoodconnect)(not(hascriminalrecord))(at island sailor)(not(hasintoxication))(not(hasdependence)))
        :effect (and(hashappiness))
    
    )
    
     (:action goal_cocaine
        :parameters (?where ?who)
        :precondition (and(at ?where ?who)(hascocaine)(hasdependence)(hasmeetsmuggler)(hasgoldbrick)(hasfrigate))
        :effect (and(hashappiness))
    )
    
    (:action goal_admiral
        :parameters (?where ?who)
        :precondition (and (at ?where ?who)(iscapitan)(haswinpirates)(at academy sailor)(not(hasintoxication)))
        :effect (and(hashappiness))
    )
     
    
    
    
    
)
