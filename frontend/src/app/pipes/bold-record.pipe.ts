import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
    name: 'boldRecord',
    standalone: true
})
export class BoldRecordPipe implements PipeTransform {
    transform(value: number | undefined, record: number | undefined, qualified = true, max: boolean = true, round: boolean = false, digits = 0) {
        const factor = 10 ** digits
        if (value === undefined) {
            return undefined
        } else if (record == undefined || !qualified || (value < record && max) || (value > record && !max)) {
            return round ? (Math.round(value * factor) / factor).toFixed(digits) : value
        } else {
            return round ? `<b>${(Math.round(value * factor) / factor).toFixed(digits)}</b>` : `<b>${value}</b>`
        }
    }
}