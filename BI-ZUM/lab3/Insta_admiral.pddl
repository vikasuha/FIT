(define (problem FindHappiness)
    (:domain sailor)
    (:requirements :strips)
    (:objects sailor ship 
            port forest river pub academy city sea island beacon
            cutwood makeship pickflowers fightbear meetmap 
            stealship pangold sober
            work salebear salecoconuts meetsmuggler
            buyalko buyconnect hardeninbattle
            accumulate invest stealmoney buyindulgence drunkcity 
            study
            losingpirates joinpirates winpirates sinkforpearl
            dazzlegirl
            collectcoconuts findcocaine
            goal_marry goal_admiral goal_cocaine
            
    )
    
    
    (:init
        (place port)
        (place forest)
        (place river)
        (place pub)
        (place academy)
        (place city)
        (place sea)
        (place island)
        (place beacon)
        (path forest river)
        (path river forest)
        (path river port)
        (path port river)
        (path port pub)
        (path pub port)
        (path port city)
        (path city port)
        (path city academy)
        (path academy city)
        
        (seapath port sea)
        (seapath sea port)
        (seapath sea island)
        (seapath island sea)
        (seapath sea beacon)
        (seapath beacon sea)
        (seapath port beacon)
        (seapath beacon port)
        
        (atplacecan forest cutwood)
        (atplacecan forest makeship)
        (atplacecan forest pickflowers)
        (atplacecan forest fightbear)
        (atplacecan forest meetmap)
        
        (atplacecan river stealship)
        (atplacecan river pangold)
        (atplacecan river sober)
        
        (atplacecan port work)
        (atplacecan port salecoconuts)
        (atplacecan port salebear)
        (atplacecan port meetsmuggler)
        
        (atplacecan pub buyalko)
        (atplacecan pub buyconnect)
        (atplacecan pub hardeninbattle)
        
        (atplacecan city accumulate)
        (atplacecan city invest)
        (atplacecan city stealmoney)
        (atplacecan city buyindulgence)
        (atplacecan city drunkcity)
        
        (atplacecan academy study)
        
        (atplacecan sea losingpirates)
        (atplacecan sea joinpirates)
        (atplacecan sea winpirates)
        ;(atplacecan sea sinkforpearl)
        (atplacecan sea sober)
        
        (atplacecan beacon dazzlegirl)
        
        (atplacecan island cutwood)
        (atplacecan island collectcoconuts)
        (atplacecan island findcocaine)
        
        (sailor sailor)
        (at port sailor)
    )
    
    (:goal (and(hashappiness)))
    
    ;(:goal (and (hasdazzlegirl)(hasgoldbrick)(haspearl)(hasflower)(hasgoodconnect)(not(hascriminalrecord))(at island sailor)(not(hasintoxication))(not(hasdependence))))
    
    ;(:goal (and(hascocaine)(hasdependence)(hasmeetsmuggler)(hasgoldbrick)(hasfrigate)))
    
    ;(:goal (and (iscapitan)(haswinpirates)(at academy sailor)(not(hasintoxication))))
    

)
