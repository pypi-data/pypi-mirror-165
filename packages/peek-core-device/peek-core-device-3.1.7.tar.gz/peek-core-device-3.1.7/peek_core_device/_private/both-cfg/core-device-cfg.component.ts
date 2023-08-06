import { Component } from "@angular/core"
import { HeaderService } from "@synerty/peek-plugin-base-js"
import { NgLifeCycleEvents } from "@synerty/vortexjs"

@Component({
    selector: "peek-core-device-cfg",
    templateUrl: "core-device-cfg.component.web.html"
})
export class CoreDeviceCfgComponent extends NgLifeCycleEvents {
    
    constructor(private headerService: HeaderService) {
        super()
        
        this.headerService.setTitle("Core Device Config")
    }
}
