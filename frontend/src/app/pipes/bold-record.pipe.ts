import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
    name: 'boldRecord',
    standalone: true
})
export class BoldRecordPipe implements PipeTransform {
    transform(value: number, record: number | undefined, max: boolean = true) {
        if (record == undefined || (value < record && max) || (value > record && !max)) {
            return value
        } else {
            return `<b>${value}</b>`
        }
    }
}