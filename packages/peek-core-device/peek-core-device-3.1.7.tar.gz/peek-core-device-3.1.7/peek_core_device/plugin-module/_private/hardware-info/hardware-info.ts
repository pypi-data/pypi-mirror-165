import {
    addTupleType,
    Tuple,
    TupleOfflineStorageService,
    TupleSelector,
} from "@synerty/vortexjs";
import { deviceTuplePrefix } from "../PluginNames";
import { Md5 } from "ts-md5/dist/md5";
import { isField as isFieldStatic } from "./is-field.mweb";
import { Capacitor } from "@capacitor/core";
import { Device } from "@capacitor/device";

export enum DeviceTypeEnum {
    MOBILE_WEB,
    FIELD_IOS,
    FIELD_ANDROID,
    DESKTOP_WEB,
    DESKTOP_WINDOWS,
    DESKTOP_MACOS,
}

export function isWeb(type: DeviceTypeEnum): boolean {
    return (
        type == DeviceTypeEnum.MOBILE_WEB || type == DeviceTypeEnum.DESKTOP_WEB
    );
}

export function isField(type: DeviceTypeEnum): boolean {
    return (
        type == DeviceTypeEnum.MOBILE_WEB ||
        type == DeviceTypeEnum.FIELD_IOS ||
        type == DeviceTypeEnum.FIELD_ANDROID
    );
}

export function isOffice(type: DeviceTypeEnum): boolean {
    return (
        type == DeviceTypeEnum.DESKTOP_MACOS ||
        type == DeviceTypeEnum.DESKTOP_WINDOWS ||
        type == DeviceTypeEnum.DESKTOP_WEB
    );
}

@addTupleType
class DeviceUuidTuple extends Tuple {
    public static readonly tupleName = deviceTuplePrefix + "DeviceUuidTuple";

    uuid: string;

    constructor() {
        super(DeviceUuidTuple.tupleName);
    }
}

export class HardwareInfo {
    private gettingWebUuidPromise: Promise<string> | null = null;
    private _webUuid: string | null = null;

    constructor(private tupleStorage: TupleOfflineStorageService) {}

    isWeb(): boolean {
        return isWeb(this.deviceType());
    }

    isField(): boolean {
        return isField(this.deviceType());
    }

    isOffice(): boolean {
        return isOffice(this.deviceType());
    }

    async uuid(): Promise<string> {
        // Wait for the platform to initialise
        const info = await Device.getInfo();

        if (info.platform === "web")
            return await this.webUuid(this.tupleStorage);

        // Wait for the platform to initialise
        return (await Device.getId()).uuid;
    }

    description(): string {
        return navigator.userAgent;
    }

    deviceType(): DeviceTypeEnum {
        // Field
        if (isFieldStatic) {
            switch (Capacitor.getPlatform()) {
                case "ios":
                    return DeviceTypeEnum.FIELD_IOS;
                case "android":
                    return DeviceTypeEnum.FIELD_ANDROID;
                case "web":
                default:
                    return DeviceTypeEnum.MOBILE_WEB;
            }
        }
        // Office
        else {
            return DeviceTypeEnum.DESKTOP_WEB;
        }
    }

    private async webUuid(
        tupleStorage: TupleOfflineStorageService
    ): Promise<string> {
        if (this._webUuid != null) return this._webUuid;

        if (this.gettingWebUuidPromise != null) {
            return this.gettingWebUuidPromise;
        }

        this.gettingWebUuidPromise = new Promise<string>(
            async (resolve, reject) => {
                const tupleSelector = new TupleSelector(
                    DeviceUuidTuple.tupleName,
                    {}
                );
                const tuples: DeviceUuidTuple[] = <DeviceUuidTuple[]>(
                    await tupleStorage //
                        .loadTuples(tupleSelector)
                );

                // If we have a UUID already, then use that.
                if (tuples.length != 0) resolve(tuples[0].uuid);

                // We don't need a real good way of getting the UUID, Peek just assigns it a token
                const browser = navigator.userAgent.substr(
                    0,
                    navigator.userAgent.indexOf(" ")
                );
                const uuid = <string>(
                    Md5.hashStr(`${browser} ${new Date().toString()}`)
                );

                // Create a new tuple to store
                const newTuple = new DeviceUuidTuple();
                newTuple.uuid = uuid;

                // Store the UUID, and upon successful storage, return the generated uuid
                await tupleStorage.saveTuples(tupleSelector, [newTuple]);
                resolve(uuid);
            }
        );

        this._webUuid = await this.gettingWebUuidPromise;
        this.gettingWebUuidPromise = null;
        return this._webUuid;
    }
}
