import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
    name: 'colname',
    standalone: true
})
export class ColNamePipe implements PipeTransform {

    transform(header: string) {
        if (header === "season") {return "Season";}
        if (header === "goals") {return "Goals";}
        if (header === "primaryAssists") {return "Pr. Assists";}
        if (header === "secondaryAssists") {return "Sec. Assists";}
        if (header === "hits") {return "Hits";}
        if (header === "sog") {return "SOG";}
        if (header === "blocks") {return "Blocks";}
        if (header === "penaltyMinutes") {return "PIM";}
        if (header === "takeaways") {return "Takeaways";}
        if (header === "giveaways") {return "Giveaways";}
        else return header;
    }

}